use anyhow::{Context, Result};

use oxiida::{
    lang::{lex::LalrLexer, parser::parse_stmt},
    runtime::{
        self,
        ffi::{CallMsg, CallSpec, FFIActor, FFIHandler},
        FilePersistence, PersistenceHandler, VarEnv,
    },
};
use pyo3::{
    exceptions::PyRuntimeError,
    ffi::c_str,
    prelude::*,
    types::{PyDict, PyTuple},
};
use serde_pyobject::{from_pyobject, to_pyobject};
use tokio::sync::mpsc;

struct PyCallActor {
    receiver: mpsc::Receiver<CallMsg>,

    // The locals here need to be a `Send`, the PyDict is not Send.
    // Py<PyDict> is detached from GIL and can cross the thread boundary.
    // This make python functions can run natively by tokio multithreading with thread steal.
    locals: Py<PyDict>,
}

impl PyCallActor {
    fn new(locals: Py<PyDict>, rx: mpsc::Receiver<CallMsg>) -> Self {
        PyCallActor {
            receiver: rx,
            locals,
        }
    }
}

impl FFIActor for PyCallActor {
    async fn receive(&mut self) -> Option<CallMsg> {
        self.receiver.recv().await
    }

    fn handle_message(&self, msg: CallMsg) {
        // increment Py reference counter, clone must inside GIL
        let locals = Python::with_gil(|py| self.locals.clone_ref(py));

        tokio::task::spawn_blocking(move || {
            match run_python_call(&msg.payload, &locals) {
                Ok(result) => {
                    // Ignoring send-errors is fine: it only happens if the caller
                    // already dropped the receiver.
                    let _ = msg.reply_to.send(result);
                }
                Err(err) => {
                    // XXX: if actor runs in daemon, the eprint will goes to logs there.
                    // How to have a nice way to make it easy to be noticed by the end user?
                    // I also need to think about the error value send back to the oxiida rt,
                    // how the runtime deal with it? How it downcast as an proper error type?
                    let _ = msg.reply_to.send(serde_json::json!(format!("{err}")));
                    eprintln!("python call except: {err}");
                    // FIXME: this drastic exit is not good it kill other processes.
                    // Better is send a structured error back and leave the run function to return
                    // an error.
                    std::process::exit(85)
                }
            }
        });
    }
}

// a sync fn calls python function in a gil of spawn_blocking thread
fn run_python_call(
    payload: &serde_json::Value,
    locals: &Py<PyDict>,
) -> anyhow::Result<serde_json::Value> {
    let payload = payload.clone();
    let spec: CallSpec =
        serde_json::from_value(payload).context("unable to convert payload to CallSpec")?;

    Python::with_gil(|py| {
        let func_name = spec.function;

        let func = if let Some(ref module) = spec.module {
            let module = py
                .import(module)
                .context(format!("unable to load module '{module}'"))?;
            module
                .getattr(&func_name)
                .context(format!("unable to load function '{}'", &func_name))?
        } else {
            let locals = locals.bind(py);
            match locals.get_item(&func_name)? {
                Some(func_name) => func_name,
                None => {
                    return Err(PyErr::new::<pyo3::exceptions::PyKeyError, _>(format!(
                        "function '{}' not found in locals",
                        &func_name
                    ))
                    .into());
                }
            }
        };

        let py_args: Vec<_> = spec
            .args
            .iter()
            .map(|v| to_pyobject(py, v))
            .collect::<Result<_, _>>()?;

        let py_args = PyTuple::new(py, &py_args)?;

        let py_result = func.call1(py_args).context("func call fail")?;
        // TODO: check and understand how this serde_pyobject crate works
        let json = from_pyobject(py_result).context("unable to convert result to json value")?;
        Ok(json)
    })
}

#[pyfunction(signature = (workflow, locals = None))]
fn run<'py>(py: Python<'py>, workflow: &str, locals: Option<Bound<'py, PyDict>>) -> PyResult<()> {
    let py_locals: Py<PyDict> = {
        let gil_locals = match locals {
            Some(b) => b,
            None => py
                .eval(
                    c_str!("__import__('inspect').currentframe().f_back.f_locals"),
                    None,
                    None,
                )?
                .downcast_into::<PyDict>()?,
        };
        gil_locals.unbind() // make it a Py<PyDict>, to detach from GIL
    };
    // dbg!(py_locals);

    // avoid it become dangling when GIL dropped
    let workflow = workflow.to_owned();
    let py_varenv_set = py_locals
        .bind_borrowed(py)
        .keys()
        .iter()
        .filter_map(|key| key.extract::<String>().ok())
        .collect();

    // `run` is call from python therefore hold the GIL, but thread spawned
    // inside message handler also request for a GIL, but this thread never release it, deadlock.
    py.allow_threads(move || -> PyResult<_> {
        let rt = tokio::runtime::Builder::new_current_thread()
            .enable_all()
            .build()
            .unwrap();

        // must goes before actors initialization where rt is needed to spawn tasks.
        let _guard = rt.enter();

        let lexer = LalrLexer::new(&workflow);
        let stmts =
            parse_stmt(lexer, &workflow).map_err(|err| PyRuntimeError::new_err(err.to_string()))?;

        let local_set = tokio::task::LocalSet::new();
        let mut glb_var_env = VarEnv::new(py_varenv_set);

        #[allow(clippy::redundant_closure)]
        let persistence_handler = PersistenceHandler::new(|rx| FilePersistence::new(rx));
        let ffi_handler = FFIHandler::new("python", |rx| PyCallActor::new(py_locals, rx));

        rt.block_on(async {
            local_set
                .run_until(async {
                    runtime::interpret(
                        stmts,
                        &mut glb_var_env,
                        persistence_handler,
                        ffi_handler,
                        &workflow,
                    )
                    .await
                    .unwrap_or_else(|err| {
                        eprintln!("{err:?}");
                    });
                })
                .await;
        });

        Ok(())
    })
}

#[pymodule(name = "oxiida")]
fn pyoxiida(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(run, m)?)?;
    Ok(())
}
