use std::{collections::HashMap, ops::RangeInclusive};

use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone)]
pub enum Stmt {
    ExprStmt(Expression),
    PrintStmt(Expression),
    SeqBlock(Vec<Stmt>),
    ParaBlock(Vec<Stmt>),
    IfStmt {
        condition: Expression,
        ifsec: Box<Stmt>,
        elsesec: Option<Box<Stmt>>,
    },
    WhileStmt {
        condition: Expression,
        body: Box<Stmt>,
    },
    ForStmt {
        x: Expression,
        xs: Expression,
        body: Box<Stmt>,
    },
    RequireStmt(Vec<String>),
    // ReturnStmt {
    //     expr: Option<Expression>,
    // },
}

// FIXME: how this compare to directly use serde_json::Value??
// If the value is the only place serde_json used, then implement Value myself here
// or if serde_json cover all cases, just make in an inner of this Value.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum Value {
    Array(Vec<Value>),
    String(String),
    Number(f64),
    Boolean(bool),
    Dict(HashMap<String, Value>),
    Nil,
}

impl From<serde_json::Value> for Value {
    fn from(value: serde_json::Value) -> Self {
        match value {
            serde_json::Value::Null => Value::Nil,
            serde_json::Value::Bool(b) => Value::Boolean(b),
            serde_json::Value::Number(n) => {
                Value::Number(n.as_f64().expect("JSON number is out of f64 range"))
            }
            serde_json::Value::String(s) => Value::String(s),
            serde_json::Value::Array(vec) => {
                Value::Array(vec.into_iter().map(Value::from).collect())
            }
            serde_json::Value::Object(map) => {
                Value::Dict(map.into_iter().map(|(k, v)| (k, Value::from(v))).collect())
            }
        }
    }
}

impl From<Value> for serde_json::Value {
    fn from(value: Value) -> Self {
        match value {
            Value::Nil => serde_json::Value::Null,
            Value::Boolean(b) => serde_json::Value::Bool(b),
            Value::Number(n) => serde_json::Value::Number(
                serde_json::Number::from_f64(n).expect("Cannot convert f64 to serde_json::Number"),
            ),
            Value::String(s) => serde_json::Value::String(s),
            Value::Array(arr) => {
                serde_json::Value::Array(arr.into_iter().map(serde_json::Value::from).collect())
            }
            Value::Dict(map) => serde_json::Value::Object(
                map.into_iter()
                    .map(|(k, v)| (k, serde_json::Value::from(v)))
                    .collect(),
            ),
        }
    }
}

impl std::fmt::Display for Value {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Value::Array(vs) => {
                let vs = vs.iter().map(|v| format!("{v}")).collect::<Vec<String>>();
                let vs = vs.join(", ");
                write!(f, "[{vs}]")
            }
            Value::Number(n) =>
            {
                #[allow(clippy::float_cmp)]
                if *n == n.trunc() {
                    write!(f, "{n}.0")
                } else {
                    write!(f, "{n}")
                }
            }
            Value::Boolean(b) => {
                write!(f, "{b}")
            }
            Value::String(s) => {
                write!(f, "\"{s}\"")
            }
            Value::Dict(items) => {
                let items = items
                    .iter()
                    .map(|(k, v)| format!("{k} -> {v}"))
                    .collect::<Vec<String>>();
                let kv = items.join(", ");
                write!(f, "{{ {kv} }}")
            }
            Value::Nil => {
                write!(f, "nil")
            }
        }
    }
}

#[derive(Debug, Clone)]
pub enum Expression {
    AssignExpr {
        lval: Box<Expression>,
        rval: Box<Expression>,
    },
    BinaryOpExpr {
        lexpr: Box<Expression>,
        op: Operator,
        rexpr: Box<Expression>,
    },
    UnaryOpExpr {
        op: Operator,
        rexpr: Box<Expression>,
    },
    Attribute {
        val: Box<Expression>,
        attr: String,
    },
    FnCallExpr {
        callee: Box<Expression>,
        args: Vec<Expression>,
        range: RangeInclusive<usize>,
    },
    ShellExpr {
        cmd: Box<Expression>,
        cmd_args: Vec<Expression>,
        stdin: Option<Box<Expression>>,
    },
    LogicOpExpr {
        lexpr: Box<Expression>,
        op: Operator,
        rexpr: Box<Expression>,
    },
    Group(Box<Expression>),
    Identifier(String, RangeInclusive<usize>),
    // XXX: can exprs in arrary always eval in parallel?
    Array(Vec<Expression>),
    Terminator {
        val: Value,
        uuid: Option<Uuid>,
        range: RangeInclusive<usize>,
    },
    FFICall(String),
    Error,
}

impl Expression {
    pub(crate) fn range(&self) -> RangeInclusive<usize> {
        match self {
            // Expression::AssignExpr { lval, rval } => todo!(),
            // Expression::BinaryOpExpr { lexpr, op, rexpr } => todo!(),
            // Expression::UnaryOpExpr { op, rexpr } => todo!(),
            // Expression::Attribute { val, attr } => todo!(),
            // Expression::ShellExpr { cmd, cmd_args, stdin } => todo!(),
            // Expression::LogicOpExpr { lexpr, op, rexpr } => todo!(),
            // Expression::Group(expression) => todo!(),
            Expression::Identifier(_, range) => range.clone(),
            Expression::Terminator { range, .. } => range.clone(),
            // Expression::Array(vec) => todo!(),
            // Expression::Error => todo!(),
            _ => todo!(),
        }
    }
}

#[derive(Debug, Clone)]
pub struct Operator {
    pub op: Op,
    pub range: RangeInclusive<usize>,
}

#[derive(Debug, Copy, Clone)]
pub enum Op {
    Mul,
    Div,
    Plus,
    Minus,
    Pow,
    Log,
    EqualEqual,
    NotEqual,
    Less,
    LessEqual,
    Greater,
    GreaterEqual,
    Bang,
    EigenBool,
    Equal,
    Or,
    And,
}

impl std::fmt::Display for Stmt {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Stmt::ExprStmt(expression) => {
                write!(f, "{expression};")
            }
            Stmt::PrintStmt(expression) => {
                write!(f, "print {expression};")
            }
            Stmt::SeqBlock(stmts) => {
                writeln!(f, "seq begin")?;
                for stmt in stmts {
                    writeln!(f, "{stmt}")?;
                }
                write!(f, "seq end")?;
                Ok(())
            }
            Stmt::ParaBlock(stmts) => {
                writeln!(f, "para begin")?;
                for stmt in stmts {
                    writeln!(f, "{stmt}")?;
                }
                write!(f, "para end")?;
                Ok(())
            }
            Stmt::IfStmt {
                condition,
                ifsec,
                elsesec,
            } => {
                if let Some(elsesec) = elsesec {
                    write!(f, "if({condition})\n{ifsec}\nelse\n{elsesec}")
                } else {
                    write!(f, "if({condition})\n{ifsec}")
                }
            }
            Stmt::WhileStmt { condition, body } => {
                write!(f, "while ({condition}) \n{body}")
            }
            Stmt::ForStmt { x, xs, body } => {
                write!(f, "for {x} in {xs}\n{body}")
            }
            // Stmt::ReturnStmt { expr } => {
            //     let nil = Expression::Terminator(Terminator::Nil);
            //     write!(f, "return {}", expr.clone().unwrap_or(nil))
            // }
            Stmt::RequireStmt(xs) => {
                let xs = xs.join(", ");
                writeln!(f, "require {xs}")
            },
        }
    }
}

impl std::fmt::Display for Expression {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Expression::AssignExpr { lval, rval } => {
                write!(f, "({lval} <- {rval})")
            }
            Expression::ShellExpr {
                cmd,
                cmd_args,
                stdin,
            } => {
                let cmd_args = cmd_args
                    .iter()
                    .map(|arg| format!("{arg}"))
                    .collect::<Vec<_>>()
                    .join(" ");
                if let Some(stdin) = stdin {
                    write!(f, "<| :exec: {cmd} {cmd_args} <<< {stdin} |>")
                } else {
                    write!(f, "<| :exec: {cmd} {cmd_args} |>")
                }
            }
            Expression::Attribute { val, attr } => {
                write!(f, "{val}.{attr}")
            }
            Expression::BinaryOpExpr { lexpr, op, rexpr }
            | Expression::LogicOpExpr { lexpr, op, rexpr } => {
                write!(f, "({op} {lexpr} {rexpr})")
            }
            Expression::UnaryOpExpr { op, rexpr } => {
                write!(f, "({op} {rexpr})")
            }
            Expression::Group(expr) => {
                write!(f, "(group {expr})")
            }
            Expression::Array(expres) => {
                let expres = expres
                    .iter()
                    .map(|v| format!("{v}"))
                    .collect::<Vec<String>>();
                let expres = expres.join(", ");
                write!(f, "[{expres}]")
            }
            Expression::Identifier(var, ..) => {
                write!(f, "{var}")
            }
            Expression::Error => {
                write!(f, "error")
            }
            Expression::Terminator { val, .. } => {
                write!(f, "{val}")
            }
            Expression::FnCallExpr { callee, args, .. } => {
                let args = args
                    .iter()
                    .map(|expr| format!("{expr}"))
                    .collect::<Vec<_>>()
                    .join(", ");
                write!(f, "<| :call: {callee}({args}) |>")
            }
            Expression::FFICall(fname) => write!(f, "fficall {fname} ~>"),
        }
    }
}

impl std::fmt::Display for Op {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Op::Mul => write!(f, "*"),
            Op::Div => write!(f, "/"),
            Op::Plus => write!(f, "+"),
            Op::Minus => write!(f, "-"),
            Op::Pow => write!(f, "^"),
            Op::Log => write!(f, "log"),
            Op::EqualEqual => write!(f, "=="),
            Op::EigenBool => write!(f, "eig"),
            Op::NotEqual => write!(f, "!="),
            Op::Less => write!(f, "<"),
            Op::LessEqual => write!(f, "<="),
            Op::Greater => write!(f, ">"),
            Op::GreaterEqual => write!(f, ">="),
            Op::Bang => write!(f, "!"),
            Op::Equal => write!(f, "="),
            Op::Or => write!(f, "or"),
            Op::And => write!(f, "and"),
        }
    }
}

impl std::fmt::Display for Operator {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.op)
    }
}
