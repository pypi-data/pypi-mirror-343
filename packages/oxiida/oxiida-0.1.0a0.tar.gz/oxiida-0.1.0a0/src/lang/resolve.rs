use miette::LabeledSpan;

// inteprete expressions
use crate::lang::ast::{Declaration, Expression, Stmt, Terminator};
use std::{cell::RefCell, collections::HashMap, ops::RangeInclusive};

// scopes manage the scopes and store variable env stack information
pub type Scopes = Vec<RefCell<HashMap<String, bool>>>;

#[derive(Eq, Hash, PartialEq, Debug)]
pub struct LookupKey {
    pub name: String,
    pub range: RangeInclusive<usize>,
}

// Locals store the resolution maping variable iden, and can tell the distance between
// where it used and where it declared.
pub type Locals = HashMap<LookupKey, usize>;

#[derive(Clone)]
pub enum FuncType {
    NaN,
    Function,
}

#[allow(clippy::missing_errors_doc)]
pub fn resolve(
    declarations: &Vec<Declaration>,
    src: &str,
    scopes: &mut Scopes,
    locals: &mut Locals,
    fun_type: &FuncType,
) -> Result<(), miette::Error> {
    for declaration in declarations {
        match declaration {
            Declaration::VarDecl { iden, rval, range } => {
                let scope = scopes
                    .last()
                    .expect("prog itself has its own scope when enter");

                if scope.borrow_mut().insert(iden.to_string(), false).is_some() && scopes.len() > 1
                {
                    return Err(miette::miette!(
                        code = format!("resolve::redeclaration"),
                        labels = vec![LabeledSpan::at(range.clone(), "this")],
                        "'{}': Already a variable with this name in this scope.",
                        iden
                    )
                    .with_source_code(src.to_string()));
                }

                if let Some(rval) = rval {
                    resolve_expr(rval.clone(), src, scopes, locals)?;
                }
                // after success initializer resolve, var is then ready
                // in order to avoid use var in initializer before resolve.
                scope.borrow_mut().insert(iden.to_string(), true);
            }
            Declaration::Stmt(stmt) => resolve_stmt(stmt.clone(), src, scopes, locals, fun_type)?,
            Declaration::FnDecl { iden, params, body } => {
                // declare eagerly so the function can call itself recursively
                let scope = scopes
                    .last()
                    .expect("prog itself has its own scope when enter");
                scope.borrow_mut().insert(iden.to_string(), true);

                // declare params for inner scope
                let mut scope = HashMap::new();

                for param in params {
                    // TODO: error for redefine function in the same scope
                    if scope.insert(param.to_string(), true).is_some() {
                        return Err(miette::miette!(
                            code = format!("resolve::fnredeclaration"),
                            "'{}': Already a variable with this name in this scope.",
                            iden
                        )
                        .with_source_code(src.to_string()));
                    }
                }
                scopes.push(RefCell::new(scope));

                resolve(body, src, scopes, locals, &FuncType::Function)?;
                scopes.pop();
            }
        }
    }
    Ok(())
}

#[allow(clippy::missing_errors_doc, clippy::too_many_lines)]
pub fn resolve_stmt(
    stmt: Stmt,
    src: &str,
    scopes: &mut Scopes,
    locals: &mut Locals,
    fun_type: &FuncType,
) -> Result<(), miette::Error> {
    match stmt {
        Stmt::ExprStmt(expression) => {
            resolve_expr(expression, src, scopes, locals)?;
            Ok(())
        }
        Stmt::PrintStmt(expression) => {
            resolve_expr(expression, src, scopes, locals)?;
            Ok(())
        }
        Stmt::Block(decls) => {
            scopes.push(RefCell::new(HashMap::new()));
            resolve(&decls, src, scopes, locals, fun_type)?;
            scopes.pop();
            Ok(())
        }
        Stmt::IfStmt {
            condition,
            ifsec,
            elsesec,
        } => {
            // release the mut borrow after eval cond expr
            resolve_expr(condition, src, scopes, locals)?;
            resolve_stmt(*ifsec, src, scopes, locals, fun_type)?;

            if let Some(elsesec) = elsesec {
                resolve_stmt(*elsesec, src, scopes, locals, fun_type)?;
            }
            Ok(())
        }
        Stmt::WhileStmt { condition, body } => {
            scopes.push(RefCell::new(HashMap::new()));
            resolve_expr(condition, src, scopes, locals)?;
            resolve_stmt(*body, src, scopes, locals, fun_type)?;
            scopes.pop();
            Ok(())
        }
        Stmt::ForStmt {
            initializer,
            condition,
            increment,
            body,
        } => {
            scopes.push(RefCell::new(HashMap::new()));
            if let Some(initializer) = initializer {
                resolve(&vec![*initializer], src, scopes, locals, fun_type)?;
            }
            resolve_expr(condition, src, scopes, locals)?;
            resolve_stmt(*body, src, scopes, locals, fun_type)?;

            if let Some(increment) = increment {
                resolve_expr(increment, src, scopes, locals)?;
            }
            scopes.pop();
            Ok(())
        }
        Stmt::ReturnStmt { expr } => {
            if matches!(fun_type, FuncType::NaN) {
                return Err(miette::miette!(
                    code = format!("resolve_stmt::returnfromtoplevel"),
                    "Can't return from top-level code."
                )
                .with_source_code(src.to_string()));
            }

            if let Some(expr) = expr {
                resolve_expr(expr, src, scopes, locals)?;
            }
            Ok(())
        }
    }
}

#[allow(clippy::too_many_lines, clippy::missing_errors_doc)]
pub fn resolve_expr(
    expr: Expression,
    src: &str,
    scopes: &Scopes,
    locals: &mut Locals,
) -> Result<(), miette::Error> {
    match expr {
        Expression::AssignExpr { lval, rval } => {
            resolve_expr(*rval, src, scopes, locals)?;
            resolve_expr(*lval, src, scopes, locals)?;
            Ok(())
        }
        Expression::LogicOpExpr {
            lhs,
            operator: _,
            rhs,
        }
        | Expression::BinaryOpExpr {
            lhs,
            operator: _,
            rhs,
        } => {
            resolve_expr(*lhs, src, scopes, locals)?;
            resolve_expr(*rhs, src, scopes, locals)?;
            Ok(())
        }
        Expression::UnaryOpExpr { operator: _, rhs } => {
            resolve_expr(*rhs, src, scopes, locals)?;
            Ok(())
        }
        Expression::Group(expression) => {
            resolve_expr(*expression, src, scopes, locals)?;
            Ok(())
        }
        Expression::FnCallExpr { callee, args, .. } => {
            resolve_expr(*callee, src, scopes, locals)?;
            for arg in args {
                resolve_expr(arg, src, scopes, locals)?;
            }
            Ok(())
        }
        Expression::FnObjExpr(..) => unreachable!(),
        Expression::Terminator(Terminator::Identifier(ref name, range)) => {
            // dbg!(&scopes);
            let scope = scopes
                .last()
                .expect("prog itself has its own scope when enter");

            // XXX: scopes.len > 1 is only for codecrafter test, it treat the innermost
            // scope as global env, but I use a dedicate env as the glb env.
            if matches!(scope.borrow().get(name), Some(false)) && scopes.len() > 1 {
                return Err(miette::miette!(
                    code = format!("resolve::resolveown"),
                    labels = vec![LabeledSpan::at(range.clone(), "this")],
                    "Can't read local variable in its own initializer."
                )
                .with_source_code(src.to_string()));
            }

            // compute the distance of reference target of the variable
            // pretty neat!! functional like syntax of rs make it naturally meaningful for distance.
            for (distance, scope) in scopes.iter().rev().enumerate() {
                // dbg!(name);
                if scope.borrow().get(name).is_some() {
                    locals.insert(
                        LookupKey {
                            name: name.to_string(),
                            range: range.clone(),
                        },
                        distance,
                    );

                    // no break, will lead to outer most found.
                    break;
                }
            }

            Ok(())
        }
        Expression::Terminator(_) => Ok(()),
    }
}
