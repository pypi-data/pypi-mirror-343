use miette::{IntoDiagnostic, LabeledSpan, Severity};
use std::collections::{HashMap, HashSet};
use std::{future::Future, pin::Pin};
use tracing::instrument;
use uuid::Uuid;

use crate::lang::ast::{self, Expression, Op, Operator, Stmt, Value};
use crate::runtime::arithmetic::BinaryTask;
use crate::runtime::core::{launch, DriveMode};
use crate::runtime::ffi::CallSpec;
use crate::runtime::shell::ShellTask;
use crate::runtime::{Entry, PersistenceHandler};

use super::arithmetic::BaseTyp;
use super::ffi::FFIHandler;
use super::shell;

#[derive(Debug, Clone)]
pub struct VarEnv {
    ffi: HashSet<String>,
    glb: HashMap<String, Expression>,
}

impl VarEnv {
    #[must_use]
    pub fn new(ffi: HashSet<String>) -> Self {
        VarEnv {
            ffi,
            glb: HashMap::new(),
        }
    }
    pub fn insert(&mut self, k: String, v: Expression) -> Option<Expression> {
        self.glb.insert(k, v)
    }

    #[must_use]
    pub fn get_glb(&self, k: &String) -> Option<&Expression> {
        self.glb.get(k)
    }

    pub fn remove(&mut self, k: &String) -> Option<Expression> {
        self.glb.remove(k)
    }

    #[must_use]
    pub fn in_ffi(&self, k: &String) -> bool {
        self.ffi.contains(k)
    }
}

pub fn interpret<'a>(
    stmts: Vec<Stmt>,
    var_env: &'a mut VarEnv,
    persistence: PersistenceHandler,
    // TODO: make a null FFIHandler so it can be consistence with persistence handler and with ffi
    // of VarEnv.
    ffi: FFIHandler,
    source_code: &'a str,
) -> Pin<Box<dyn Future<Output = Result<(), miette::Error>> + 'a>> {
    Box::pin(async move {
        for stmt in stmts {
            let persistence = persistence.clone();
            let ffi = ffi.clone();
            execute(stmt, var_env, persistence, ffi, source_code).await?;
        }
        Ok(())
    })
}

#[derive(Debug)]
pub enum ControlFlow {
    Continue,
    Return(Expression),
}

// XXX: think, do I need to return Expression for the execute? it can be handy. Nil for none return
// type.
//
// Note: to proper implement generic for persistence, the uuid have to be generate for the every
// new terminator value, if user has no any intersted on the provenance, this is the overhead.
// Even with NullPersistence, I try to use uuid. Simply because to distinguish not generate uuid
// case the API is not extremly consistence. I need allow passing persistence as an option.
// TODO: One option is to have NullPersistence insert with return None for uuid, and in the
// NullPersistence implementation, just do not use uuid but directly return None.
// Meanwhile, the clone of the value to store into the persistence system require heap allocation
// which also bring the overhead.
#[instrument(level = "trace", skip(persistence))]
pub fn execute<'a>(
    stmt: Stmt,
    var_env: &'a mut VarEnv,
    persistence: PersistenceHandler,
    ffi: FFIHandler,
    source_code: &'a str,
) -> Pin<Box<dyn Future<Output = Result<ControlFlow, miette::Error>> + 'a>> {
    Box::pin(async move {
        match stmt {
            Stmt::SeqBlock(stmts) => {
                for stmt in stmts {
                    let persistence = persistence.clone();
                    let ffi = ffi.clone();
                    execute(stmt, var_env, persistence, ffi, source_code).await?;
                }
                Ok(ControlFlow::Continue)
            }
            Stmt::ParaBlock(stmts) => {
                let futures: Vec<_> = stmts
                    .into_iter()
                    .map(|stmt| {
                        let mut var_env = var_env.clone();
                        let persistence = persistence.clone();
                        let ffi = ffi.clone();
                        async move {
                            execute(stmt, &mut var_env, persistence, ffi, source_code).await
                        }
                    })
                    .collect();

                futures::future::join_all(futures).await;
                Ok(ControlFlow::Continue)
            }
            Stmt::ExprStmt(expr) => {
                eval(
                    expr,
                    var_env,
                    persistence.clone(),
                    ffi.clone(),
                    source_code,
                )
                .await?;
                Ok(ControlFlow::Continue)
            }
            Stmt::PrintStmt(expr) => {
                let expr = eval(
                    expr,
                    var_env,
                    persistence.clone(),
                    ffi.clone(),
                    source_code,
                )
                .await?;
                if let Expression::Terminator {
                    val: Value::String(s),
                    ..
                } = expr
                {
                    // " should not include when print string
                    let s = s.trim_start_matches('"').trim_end_matches('"');
                    println!("{s}");
                    Ok(ControlFlow::Continue)
                } else {
                    println!("{expr}");
                    Ok(ControlFlow::Continue)
                }
            }
            Stmt::IfStmt {
                condition,
                ifsec,
                elsesec,
            } => {
                // release the mut borrow after eval cond expr
                let cond = {
                    let condition = Expression::UnaryOpExpr {
                        op: Operator {
                            op: Op::EigenBool,
                            range: 0..=0,
                        },
                        rexpr: Box::new(condition),
                    };
                    eval(
                        condition,
                        var_env,
                        persistence.clone(),
                        ffi.clone(),
                        source_code,
                    )
                    .await?
                };

                match cond {
                    Expression::Terminator {
                        val: Value::Boolean(b),
                        ..
                    } => match (b, elsesec) {
                        (true, _) => {
                            execute(
                                *ifsec,
                                var_env,
                                persistence.clone(),
                                ffi.clone(),
                                source_code,
                            )
                            .await?;
                            Ok(ControlFlow::Continue)
                        }
                        (false, Some(elsesec)) => {
                            execute(
                                *elsesec,
                                var_env,
                                persistence.clone(),
                                ffi.clone(),
                                source_code,
                            )
                            .await?;
                            Ok(ControlFlow::Continue)
                        }
                        (false, None) => {
                            // XXX: how? needed by return, do I need return in workflow DSL?
                            // Ok(ControlFlow::Continue)
                            Ok(ControlFlow::Continue)
                        }
                    },
                    expr => {
                        Err(miette::miette!(
                            code = "interpret::ifelsecondition",
                            // TODO: labels = vec![LabeledSpan::at(range, "this")],
                            "{expr} is not a valid condition"
                        )
                        .with_source_code(source_code.to_owned()))
                    }
                }
            }
            Stmt::WhileStmt { condition, body } => {
                loop {
                    // release the mut borrow after eval cond expr
                    let cond = {
                        let incond = Expression::UnaryOpExpr {
                            op: Operator {
                                op: Op::EigenBool,
                                range: 0..=0,
                            },
                            rexpr: Box::new(condition.clone()),
                        };
                        eval(
                            incond,
                            var_env,
                            persistence.clone(),
                            ffi.clone(),
                            source_code,
                        )
                        .await?
                    };

                    match cond {
                        Expression::Terminator {
                            val: Value::Boolean(b),
                            ..
                        } => {
                            if b {
                                let persistence = persistence.clone();
                                let ffi = ffi.clone();
                                let execute = execute(
                                    *body.clone(),
                                    var_env,
                                    persistence,
                                    ffi,
                                    source_code,
                                )
                                .await?;
                                match execute {
                                    ControlFlow::Continue => continue,
                                    ret @ ControlFlow::Return(_) => return Ok(ret),
                                }
                            }
                            break;
                        }
                        expr => {
                            return Err(miette::miette!(
                                code = "interpret::ifelsecondition",
                                // TODO: labels = vec![LabeledSpan::at(range, "this")],
                                "{expr} is not a valid condition"
                            )
                            .with_source_code(source_code.to_owned()));
                        }
                    }
                }
                Ok(ControlFlow::Continue)
            }
            Stmt::ForStmt { x, xs, body } => {
                let xs = eval(
                    xs,
                    var_env,
                    persistence.clone(),
                    ffi.clone(),
                    source_code,
                )
                .await?;
                if let (Expression::Identifier(ref var_x, range), Expression::Array(xs)) = (x, xs) {
                    // since I use single level var_env instead of closure and scope.
                    // I create var_x as the local iter variable and delete after the current loop.
                    // The restriction is the local iter var should not be used before.
                    if var_env.get_glb(var_x).is_some() {
                        return Err(miette::miette!(
                            code = "rt::forstmt::redeclare::var",
                            labels = vec![LabeledSpan::at(range, "this")],
                            "cannot to redeclare '{var_x}'"
                        )
                        .with_source_code(source_code.to_owned()));
                    }
                    for x in xs {
                        var_env.insert(var_x.to_string(), x);
                        execute(
                            *body.clone(),
                            var_env,
                            persistence.clone(),
                            ffi.clone(),
                            source_code,
                        )
                        .await?;
                    }
                    var_env.remove(var_x);
                } else {
                    // TODO: this should covered by the resolve inspect before runtime
                    unreachable!()
                }
                Ok(ControlFlow::Continue)
            }
            Stmt::RequireStmt(xs) => {
                for x in xs {
                    if var_env.in_ffi(&x) {
                        let pop = var_env.insert(x.clone(), Expression::FFICall(x));
                        if let Some(pop) = pop {
                            return Err(miette::miette!(
                                code = "rt::execute::require::var_exist",
                                // TODO: labels = vec![LabeledSpan::at(range, "this")],
                                "{pop} is already defined"
                            )
                            .with_source_code(source_code.to_owned()))?;
                        }
                    } else {
                        // TODO: deal with reuse workflow, not always raise.
                        return Err(miette::miette!(
                            code = "rt::execute::require::not_in_ffi",
                            // TODO: labels = vec![LabeledSpan::at(range, "this")],
                            "'{x}' not in ffi"
                        )
                        .with_source_code(source_code.to_owned()))?;
                    }
                }
                Ok(ControlFlow::Continue)
            }
        }
    })
}

#[allow(clippy::too_many_lines)]
pub fn eval<'a>(
    expr: Expression,
    var_env: &'a mut VarEnv,
    persistence: PersistenceHandler,
    ffi: FFIHandler,
    source_code: &'a str,
) -> Pin<Box<dyn Future<Output = Result<Expression, miette::Error>> + 'a>> {
    Box::pin(async move {
        let connect = async |from: Uuid, legend: Option<&str>, to: Uuid| {
            // TODO: tracing
            let _ = persistence
                .insert(Entry::Edge {
                    src: from,
                    legend: legend.map(ToString::to_string),
                    dst: to,
                })
                .await;
        };
        match expr {
            Expression::Group(expr) => {
                eval(*expr, var_env, persistence, ffi, source_code).await
            }
            Expression::BinaryOpExpr { lexpr, op, rexpr } => {
                let aval = eval(
                    *lexpr,
                    var_env,
                    persistence.clone(),
                    ffi.clone(),
                    source_code,
                )
                .await?;
                let bval = eval(
                    *rexpr,
                    var_env,
                    persistence.clone(),
                    ffi.clone(),
                    source_code,
                )
                .await?;

                let (mut task, left_uuid, right_uuid) = match (aval, bval) {
                    (
                        Expression::Terminator {
                            val: Value::Number(left),
                            uuid: left_uuid,
                            ..
                        },
                        Expression::Terminator {
                            val: Value::Number(right),
                            uuid: right_uuid,
                            ..
                        },
                    ) => {
                        let task = BinaryTask::new(&op, &left.into(), &right.into());
                        (task, left_uuid, right_uuid)
                    }
                    (
                        Expression::Terminator {
                            val: Value::String(left),
                            uuid: left_uuid,
                            ..
                        },
                        Expression::Terminator {
                            val: Value::String(right),
                            uuid: right_uuid,
                            ..
                        },
                    ) => {
                        let task = BinaryTask::new(&op, &left.into(), &right.into());
                        (task, left_uuid, right_uuid)
                    }
                    (lhs, rhs) => {
                        Err(miette::miette!(
                            severity = Severity::Error,
                            code = "rt::binary::incorrect::op",
                            // help = "casting type",
                            labels = vec![LabeledSpan::at(op.range.clone(), "here")],
                            "invalid binary operation {lhs} {op} {rhs}"
                        )
                        .with_source_code(source_code.to_owned()))?
                    }
                };

                let proc = task.proc.take().unwrap();
                let (joiner, handler) = launch(proc, DriveMode::FireAndForget);

                let _ = handler.try_nudge();

                // TODO: error handling
                let res = joiner.await.expect("task failed");
                task.output = res;
                let expr = match task.output.unwrap() {
                    BaseTyp::Number(n) => {
                        let val = Value::Number(n);
                        let task_id = persistence
                            .insert(Entry::Task {
                                name: format!("buildin: {}", &op),
                            })
                            .await;
                        let out_id = persistence.insert(Entry::Node(val.clone())).await;

                        if let Some(left_uuid) = left_uuid {
                            connect(left_uuid, Some("lhs"), task_id).await;
                        }
                        if let Some(right_uuid) = right_uuid {
                            connect(right_uuid, Some("rhs"), task_id).await;
                        }
                        connect(task_id, Some("out"), out_id).await;

                        Expression::Terminator {
                            val,
                            uuid: Some(out_id),
                            range: 0..=0,
                        }
                    }
                    BaseTyp::Bool(b) => {
                        let val = Value::Boolean(b);
                        let uuid = persistence.insert(Entry::Node(val.clone())).await;
                        Expression::Terminator {
                            val,
                            uuid: Some(uuid),
                            range: 0..=0,
                        }
                    }
                    BaseTyp::Str(s) => {
                        let val = Value::String(s);
                        let uuid = persistence.insert(Entry::Node(val.clone())).await;
                        Expression::Terminator {
                            val,
                            uuid: Some(uuid),
                            range: 0..=0,
                        }
                    }
                };
                Ok(expr)
            }
            Expression::UnaryOpExpr {
                op: operator,
                rexpr,
            } => {
                let val = eval(
                    *rexpr,
                    var_env,
                    persistence.clone(),
                    ffi,
                    source_code,
                )
                .await?;
                match (operator.op, val) {
                    (Op::Plus, expr @ Expression::Terminator { .. }) => Ok(expr),
                    (
                        Op::Minus,
                        Expression::Terminator {
                            val: Value::Number(n),
                            uuid: Some(in_id),
                            range,
                        },
                    ) => {
                        let val = Value::Number(-n);
                        let task_id = persistence
                            .insert(Entry::Task {
                                // TODO: the buildin name in one place as mapping.
                                name: "buildin: negative".to_string(),
                            })
                            .await;
                        let out_id = persistence.insert(Entry::Node(val.clone())).await;

                        connect(in_id, Some("in"), task_id).await;
                        connect(task_id, Some("out"), out_id).await;

                        Ok(Expression::Terminator {
                            val,
                            uuid: Some(out_id),
                            range,
                        })
                    }
                    (
                        Op::Bang,
                        Expression::Terminator {
                            val: Value::Boolean(b),
                            uuid: Some(in_id),
                            range,
                        },
                    ) => {
                        let val = Value::Boolean(!b);
                        let task_id = persistence
                            .insert(Entry::Task {
                                // TODO: the buildin name in one place as mapping.
                                name: "buildin: bang".to_string(),
                            })
                            .await;
                        let out_id = persistence.insert(Entry::Node(val.clone())).await;

                        connect(in_id, Some("in"), task_id).await;
                        connect(task_id, Some("out"), out_id).await;

                        Ok(Expression::Terminator {
                            val,
                            uuid: Some(out_id),
                            range,
                        })
                    }
                    (Op::EigenBool, expr) => match expr {
                        expr @ Expression::Terminator {
                            val: Value::Boolean(true | false),
                            ..
                        } => Ok(expr),
                        Expression::Terminator {
                            val: Value::Nil,
                            uuid: Some(in_id),
                            range,
                        } => {
                            let val = Value::Boolean(false);
                            let task_id = persistence
                                .insert(Entry::Task {
                                    // TODO: the buildin name in one place as mapping.
                                    name: "buildin: bang".to_string(),
                                })
                                .await;
                            let out_id = persistence.insert(Entry::Node(val.clone())).await;

                            connect(in_id, Some("in"), task_id).await;
                            connect(task_id, Some("out"), out_id).await;

                            Ok(Expression::Terminator {
                                val,
                                uuid: Some(out_id),
                                range,
                            })
                        }
                        Expression::Terminator {
                            val:
                                Value::String(_) | Value::Dict(_) | Value::Array(_) | Value::Number(_),
                            uuid: Some(in_id),
                            range,
                        } => {
                            let val = Value::Boolean(true);
                            let task_id = persistence
                                .insert(Entry::Task {
                                    // TODO: the buildin name in one place as mapping.
                                    name: "buildin: bang".to_string(),
                                })
                                .await;
                            let out_id = persistence.insert(Entry::Node(val.clone())).await;

                            connect(in_id, Some("in"), task_id).await;
                            connect(task_id, Some("out"), out_id).await;

                            Ok(Expression::Terminator {
                                val,
                                uuid: Some(out_id),
                                range,
                            })
                        }
                        _ => {
                            let val = Value::Boolean(true);
                            let uuid = persistence.insert(Entry::Node(val.clone())).await;
                            Ok(Expression::Terminator {
                                val,
                                uuid: Some(uuid),
                                range: 0..=0,
                            })
                        }
                    },
                    // TODO: branch not specific enough to cover when the the uuid is not assigned.
                    // It should be assigned in the eval above.
                    (op, v) => Err(miette::miette!(
                        code = "rt::eval::unary::invalidop",
                        labels = vec![LabeledSpan::at(operator.range, "this")],
                        "unable to eval unary expr: {op} {v}"
                    )
                    .with_source_code(source_code.to_owned()))?,
                }
            }
            Expression::LogicOpExpr { lexpr, op, rexpr } => {
                // TODO: near-fuzz tests required for shortcut
                match op.op {
                    ast::Op::Or => {
                        let aval = eval(
                            *lexpr,
                            var_env,
                            persistence.clone(),
                            ffi.clone(),
                            source_code,
                        )
                        .await?;
                        if matches!(
                            aval,
                            Expression::Terminator {
                                val: Value::Boolean(false) | Value::Nil,
                                ..
                            }
                        ) {
                            let bval = eval(
                                *rexpr,
                                var_env,
                                persistence.clone(),
                                ffi.clone(),
                                source_code,
                            )
                            .await?;
                            if matches!(
                                bval,
                                Expression::Terminator {
                                    val: Value::Boolean(false) | Value::Nil,
                                    ..
                                }
                            ) {
                                // FIXME: the presistence not properly taken care of for logic and
                                // and logic or.
                                return Ok(Expression::Terminator {
                                    val: Value::Boolean(false),
                                    uuid: None,
                                    range: 0..=0,
                                });
                            }
                            return Ok(Expression::Terminator {
                                val: Value::Boolean(true),
                                uuid: None,
                                range: 0..=0,
                            });
                        }
                        // shortcut when lhs is true
                        Ok(Expression::Terminator {
                            val: Value::Boolean(true),
                            uuid: None,
                            range: 0..=0,
                        })
                    }
                    ast::Op::And => {
                        let aval = eval(
                            *lexpr,
                            var_env,
                            persistence.clone(),
                            ffi.clone(),
                            source_code,
                        )
                        .await?;
                        if !matches!(
                            aval,
                            Expression::Terminator {
                                val: Value::Boolean(false) | Value::Nil,
                                ..
                            }
                        ) {
                            let bval = eval(
                                *rexpr,
                                var_env,
                                persistence.clone(),
                                ffi.clone(),
                                source_code,
                            )
                            .await?;
                            if !matches!(
                                bval,
                                Expression::Terminator {
                                    val: Value::Boolean(false) | Value::Nil,
                                    ..
                                }
                            ) {
                                // FIXME:
                                return Ok(Expression::Terminator {
                                    val: Value::Boolean(true),
                                    uuid: None,
                                    range: 0..=0,
                                });
                            }
                            return Ok(Expression::Terminator {
                                val: Value::Boolean(false),
                                uuid: None,
                                range: 0..=0,
                            });
                        }
                        // shortcut when lhs is false
                        Ok(Expression::Terminator {
                            val: Value::Boolean(false),
                            uuid: None,
                            range: 0..=0,
                        })
                    }
                    _ => unreachable!(),
                }
            }
            Expression::AssignExpr { lval, rval } => {
                let rval = eval(
                    *rval,
                    var_env,
                    persistence.clone(),
                    ffi.clone(),
                    source_code,
                )
                .await?;
                if let Expression::Identifier(iden, range) = *lval {
                    if var_env.in_ffi(&iden) {
                        return Err(miette::miette!(
                            code = "rt::eval::assign::var_exist_in_ffi",
                            labels = vec![LabeledSpan::at(range, "this")],
                            help = "rename the variable in your script",
                            "'{}' found in {} script, you cannot shadow it in workflow",
                            iden,
                            ffi.name
                        )
                        .with_source_code(source_code.to_owned()))?;
                    }
                    // TODO: resolve phase check
                    // Question, do I allow shadowing variable in oxiida?
                    // Pro: don't need res1, res2, ... but can shadowing.
                    // Con: potential bugs.
                    //
                    // I may take approach in the middle, allow shadowing but only for the same
                    // type.
                    var_env.insert(iden, rval.clone());
                    Ok(rval)
                } else {
                    let lval = eval(
                        *lval,
                        var_env,
                        persistence.clone(),
                        ffi.clone(),
                        source_code,
                    )
                    .await?;
                    Ok(Expression::AssignExpr {
                        lval: Box::new(lval),
                        rval: Box::new(rval),
                    })
                }
            }
            Expression::ShellExpr {
                cmd,
                cmd_args,
                stdin,
            } => {
                let cmd = eval(
                    *cmd,
                    var_env,
                    persistence.clone(),
                    ffi.clone(),
                    source_code,
                )
                .await?;
                let Expression::Terminator {
                    val: Value::String(ref cmd_lit),
                    uuid: Some(cmd_in_uuid),
                    ..
                } = cmd
                else {
                    return Err(miette::miette!(
                        code = "rt::eval::shell::cmd_only_string",
                        labels = vec![LabeledSpan::at(cmd.range(), "this")],
                        "cmd is not a string"
                    )
                    .with_source_code(source_code.to_owned()))?;
                };
                let mut evaluated_args = Vec::new();
                for arg in cmd_args {
                    let result = eval(
                        arg,
                        var_env,
                        persistence.clone(),
                        ffi.clone(),
                        source_code,
                    )
                    .await?;
                    evaluated_args.push(result);
                }
                let pairs: Result<Vec<_>, _> = evaluated_args
                    .into_iter()
                    .map(|arg| {
                        if let Expression::Terminator {
                            val: Value::String(arg),
                            uuid: arg_in,
                            ..
                        } = arg
                        {
                            Ok((arg, arg_in))
                        } else {
                            Err(miette::miette!(
                                code = "rt::eval::shell::arg_only_string",
                                labels = vec![LabeledSpan::at(cmd.range(), "this")],
                                "{arg} is not a string"
                            )
                            .with_source_code(source_code.to_owned()))
                        }
                    })
                    .collect();

                let (cmd_args, in_args): (Vec<_>, Vec<_>) = pairs?.into_iter().unzip();

                let (mut task, stdin_uuid) = if let Some(stdin) = stdin {
                    let stdin = eval(
                        *stdin,
                        var_env,
                        persistence.clone(),
                        ffi.clone(),
                        source_code,
                    )
                    .await?;
                    if let Expression::Terminator {
                        val: Value::String(stdin),
                        uuid,
                        ..
                    } = stdin
                    {
                        (ShellTask::new(cmd_lit, &cmd_args, Some(&stdin)), uuid)
                    } else {
                        return Err(miette::miette!(
                            code = "rt::eval::shell::stdin_only_string",
                            labels = vec![LabeledSpan::at(cmd.range(), "this")],
                            "stdin is not a string"
                        )
                        .with_source_code(source_code.to_owned()));
                    }
                } else {
                    (ShellTask::new(cmd_lit, &cmd_args, None), None)
                };
                let proc = task.proc.take().unwrap();
                let (joiner, handler) = launch(proc, DriveMode::FireAndForget);
                let _ = handler.try_nudge();

                // task entry
                let task_id = persistence
                    .insert(Entry::Task {
                        name: format!("shell: {{ {task} }}"),
                    })
                    .await;

                // input edge entries
                connect(cmd_in_uuid, Some("cmd"), task_id).await;
                for (idx, input) in in_args.into_iter().flatten().enumerate() {
                    connect(input, Some(format!("param_{idx}").as_str()), task_id).await;
                }
                if let Some(stdin_uuid) = stdin_uuid {
                    connect(stdin_uuid, Some("stdin"), task_id).await;
                }

                // TODO: error handling
                let res = joiner.await.expect("task failed");

                // XXX: set the the output of task, ?? maybe duplicate data twice with store it as
                // serializable data is not needed
                task.output = Some(shell::Output::from(res.unwrap()));

                if let Some(out) = task.output {
                    let val: Value = out.into();
                    let out_id = persistence.insert(Entry::Node(val.clone())).await;
                    connect(task_id, Some("out"), out_id).await;

                    Ok(Expression::Terminator {
                        val,
                        uuid: Some(out_id),
                        range: 0..=0,
                    })
                } else {
                    unreachable!()
                }
            }
            Expression::Identifier(iden, range) => {
                match (var_env.get_glb(&iden), var_env.in_ffi(&iden)) {
                    (Some(expr), _) => Ok(expr.clone()),
                    // TODO: can all be a resolve phase check for the variables
                    (None, true) => Err(miette::miette!(
                        severity = Severity::Error,
                        code = "rt::identifier::expect::var_in_ffi",
                        help = "explicitly declare variable in embeded oxiida code",
                        labels = vec![LabeledSpan::at(range.clone(), "this")],
                        "variable '{iden}' not defined in oxiida but found in script language"
                    )
                    .with_source_code(source_code.to_owned())),
                    (None, false) => Err(miette::miette!(
                        severity = Severity::Error,
                        code = "rt::identifier::expect::var",
                        help = "declare before use",
                        labels = vec![LabeledSpan::at(range.clone(), "this")],
                        "variable '{iden}' not defined"
                    )
                    .with_source_code(source_code.to_owned())),
                }
            }
            Expression::Array(exprs) => {
                let mut arr = Vec::new();
                // TODO: can in para, just put it in async move block and join all.
                for expr in exprs {
                    let value = eval(
                        expr,
                        var_env,
                        persistence.clone(),
                        ffi.clone(),
                        source_code,
                    )
                    .await?;
                    arr.push(value);
                }
                // TODO: Limit the flexibility of array by coersing that the type of elements
                // after fist round of runtime eval should be the same type.
                Ok(Expression::Array(arr))
            }
            Expression::Attribute { val, attr } => {
                // Extract an attr from a dict value create new data entry.
                let val = eval(
                    *val,
                    var_env,
                    persistence.clone(),
                    ffi.clone(),
                    source_code,
                )
                .await?;
                let expr = match val {
                    Expression::Terminator {
                        val: value,
                        uuid,
                        range,
                    } => match value {
                        Value::Dict(d) => {
                            if let Some(val) = d.get(&attr) {
                                // I can unwrap since the dict value is a terminator that already
                                // create with the valid uuid.
                                let uuid = uuid.unwrap();
                                let new_uuid = persistence.insert(Entry::Node(val.clone())).await;
                                persistence
                                    .insert(Entry::Edge {
                                        src: uuid,
                                        legend: Some(format!("--attr:'{attr}'-->")),
                                        dst: new_uuid,
                                    })
                                    .await;
                                Expression::Terminator {
                                    val: val.clone(),
                                    uuid: Some(new_uuid),
                                    range,
                                }
                            } else {
                                Err(miette::miette!(
                                    code = "rt::eval::attr::key_not_exist",
                                    labels = vec![LabeledSpan::at(range, "this")],
                                    "key {attr} not exist"
                                )
                                .with_source_code(source_code.to_owned()))?
                            }
                        }
                        _ => Err(miette::miette!(
                            code = "rt::eval::attr::not_dict",
                            labels = vec![LabeledSpan::at(range, "this")],
                            "not a dict can't get {attr} from it"
                        )
                        .with_source_code(source_code.to_owned()))?,
                    },
                    // XXX: at the moment, only support get attrs from shell res, soon will be all
                    // of customized types.
                    _ => unreachable!(),
                };
                Ok(expr)
            }
            Expression::FnCallExpr {
                callee,
                args,
                range,
            } => {
                let callee = eval(
                    *callee,
                    var_env,
                    persistence.clone(),
                    ffi.clone(),
                    source_code,
                )
                .await?;

                match callee {
                    Expression::FFICall(fncall) => {
                        let (module, fncall): (Option<String>, String) = {
                            let mut sec_iter = fncall.rsplit('.');
                            let Some(fncall) = sec_iter.next() else {
                                Err(miette::miette!(
                                    code = "rt::eval::fncall::iden_not_string",
                                    labels = vec![LabeledSpan::at(range, "this")],
                                    "empty function name"
                                )
                                .with_source_code(source_code.to_owned()))?
                            };
                            // TODO: this part is not actually used, because grammar part not
                            // support the dot seperate identifier yet.
                            let module = sec_iter.collect::<Vec<_>>().join(".");
                            let module = match module.as_str() {
                                "" => None,
                                module => Some(module.to_string()),
                            };
                            (module, fncall.to_string())
                        };

                        let mut args_arr = Vec::new();

                        // eval arg in sequence to early return if it is not resolved to serde value type.
                        for arg in args {
                            let value = eval(
                                arg,
                                var_env,
                                persistence.clone(),
                                ffi.clone(),
                                source_code,
                            )
                            .await?;
                            let value = match value {
                                Expression::Terminator { val, .. } => val.into(),
                                _ => Err(miette::miette!(
                                    code = "rt::eval::fncall::arg_not_value",
                                    labels = vec![LabeledSpan::at(range.clone(), "this")],
                                    // TODO: provide the help link
                                    "arg should be a serializable value"
                                )
                                .with_source_code(source_code.to_owned()))?,
                            };
                            args_arr.push(value);
                        }

                        let call_spec = CallSpec {
                            module,
                            function: fncall,
                            args: args_arr,
                        };
                        let val = ffi.call(&call_spec).await.into_diagnostic()?;
                        let val: Value = val.into();
                        let new_uuid = persistence.insert(Entry::Node(val.clone())).await;
                        Ok(Expression::Terminator {
                            val,
                            uuid: Some(new_uuid),
                            range: 0..=0,
                        })
                    }
                    // TODO: OxFnCall
                    _ => todo!(),
                }
            }
            Expression::Terminator { val, uuid, range } => {
                let expr = if uuid.is_none() {
                    let new_uuid = persistence.insert(Entry::Node(val.clone())).await;
                    Expression::Terminator {
                        val,
                        uuid: Some(new_uuid),
                        range,
                    }
                } else {
                    Expression::Terminator { val, uuid, range }
                };
                Ok(expr)
            }
            Expression::FFICall(..) => unreachable!(),
            expr @ Expression::Error => Ok(expr),
        }
    })
}
