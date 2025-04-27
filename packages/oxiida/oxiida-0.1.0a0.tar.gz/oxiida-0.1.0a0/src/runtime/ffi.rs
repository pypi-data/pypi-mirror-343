use serde::{Deserialize, Serialize};
use std::future::Future;
use thiserror::Error;
use tokio::sync::{mpsc, oneshot};

#[derive(Error, Debug)]
pub enum CallError {
    #[error("failed to serialize CallSpec: {0}")]
    Serialization(#[from] serde_json::Error),
    #[error("filed to send CallMsg")]
    Send,
    #[error("Actor task killed or channel closed before reply")]
    Receive,
}

#[derive(Debug)]
pub struct CallMsg {
    pub payload: serde_json::Value,
    pub reply_to: oneshot::Sender<serde_json::Value>,
}

// XXX: field names are now still python specific, better change to
// namespace, symbol
#[derive(Debug, Deserialize, Serialize)]
pub struct CallSpec {
    pub module: Option<String>,
    pub function: String,
    pub args: Vec<serde_json::Value>,
}

#[derive(Debug, Clone)]
pub struct FFIHandler {
    pub name: String,
    pub sender: mpsc::Sender<CallMsg>,
}

pub trait FFIActor: Send + 'static {
    fn receive(&mut self) -> impl Future<Output = Option<CallMsg>> + Send;
    fn handle_message(&self, msg: CallMsg);
}

pub struct NullActor {
    receiver: mpsc::Receiver<CallMsg>,
}

impl NullActor {
    #[must_use]
    pub fn new(rx: mpsc::Receiver<CallMsg>) -> Self {
        NullActor { receiver: rx }
    }
}

impl FFIActor for NullActor {
    async fn receive(&mut self) -> Option<CallMsg> {
        self.receiver.recv().await
    }

    fn handle_message(&self, _msg: CallMsg) {
        unreachable!()
    }
}

// FFIActor need to carry also the local environment in the constructor.
impl FFIHandler {
    #[must_use]
    pub fn new<A, F>(name: &str, make_actor: F) -> FFIHandler
    where
        A: FFIActor,
        F: FnOnce(mpsc::Receiver<CallMsg>) -> A,
    {
        // XXX: retrospect on the channel capacity with benchmark.
        let (tx, rx) = mpsc::channel(10);
        let actor = make_actor(rx);
        tokio::spawn(async move { run_ffi_call_actor(actor).await });

        Self {
            name: name.to_string(),
            sender: tx,
        }
    }

    /// should be pub(crate) since only call from interpret function
    /// Make it pub for test purpose to be able to call directly from `run`.
    ///
    /// # Errors
    /// TODO: errros blabla
    pub async fn call(&self, call_spec: &CallSpec) -> Result<serde_json::Value, CallError> {
        let (tx, rx) = oneshot::channel();
        let payload = serde_json::to_value(call_spec)?;

        // Ignore send errors. If this send fails, so does the
        // recv.await below. There's no reason to check for the
        // same failure twice.
        self.sender
            .send(CallMsg {
                payload,
                reply_to: tx,
            })
            .await
            .map_err(|_| CallError::Send)?;
        rx.await.map_err(|_| CallError::Receive)
    }
}

async fn run_ffi_call_actor<A>(mut actor: A)
where
    A: FFIActor,
{
    while let Some(msg) = actor.receive().await {
        // TODO: need to think how to manage the cancellation.
        actor.handle_message(msg);
    }
}
