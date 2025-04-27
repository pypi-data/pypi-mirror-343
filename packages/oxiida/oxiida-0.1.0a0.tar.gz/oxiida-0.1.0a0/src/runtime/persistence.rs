use std::{
    fs,
    future::Future,
    io::{BufWriter, Write},
    path::PathBuf,
};
use tokio::sync::{mpsc, oneshot};
use tracing::instrument;
use uuid::{NoContext, Timestamp, Uuid};

use crate::lang::ast::Value;

#[derive(Debug, Clone)]
pub enum Entry {
    Node(Value),
    Task {
        name: String,
    },
    Edge {
        src: Uuid,
        legend: Option<String>,
        dst: Uuid,
    },
}

#[derive(Debug)]
pub enum PersistenceMsg {
    Create {
        entry: Entry,
        respond_to: oneshot::Sender<Uuid>,
    },
    Get,
    Update,
    Delete,
}

#[derive(Debug, Clone)]
pub struct PersistenceHandler {
    sender: mpsc::Sender<PersistenceMsg>,
}

impl PersistenceHandler {
    #[must_use]
    pub fn new<A, F>(make_actor: F) -> PersistenceHandler
    where
        A: PersistenceActor,
        F: FnOnce(mpsc::Receiver<PersistenceMsg>) -> A,
    {
        // XXX: retrospect on the channel capacity with benchmark.
        let (tx, rx) = mpsc::channel(10);
        let actor = make_actor(rx);
        tokio::spawn(async move { run_persistence_actor(actor).await });

        Self { sender: tx }
    }

    #[instrument(skip(self))]
    pub async fn insert(&self, entry: Entry) -> Uuid {
        let (tx, rx) = oneshot::channel();

        // Ignore send errors. If this send fails, so does the
        // recv.await below. There's no reason to check for the
        // same failure twice.
        let _ = self
            .sender
            .send(PersistenceMsg::Create {
                entry: entry.clone(),
                respond_to: tx,
            })
            .await;
        rx.await.expect("Actor task has been killed")
    }

    pub async fn get() -> Option<Entry> {
        todo!()
    }
}

pub trait PersistenceActor: Send + 'static {
    fn receive(&mut self) -> impl Future<Output = Option<PersistenceMsg>> + Send;
    fn handle_message(&mut self, msg: PersistenceMsg);
}

#[derive(Debug)]
pub struct NullPersistence {
    receiver: mpsc::Receiver<PersistenceMsg>,
}

impl NullPersistence {
    #[must_use]
    pub fn new(receiver: mpsc::Receiver<PersistenceMsg>) -> Self {
        NullPersistence { receiver }
    }
}

impl PersistenceActor for NullPersistence {
    async fn receive(&mut self) -> Option<PersistenceMsg> {
        self.receiver.recv().await
    }

    fn handle_message(&mut self, msg: PersistenceMsg) {
        match msg {
            PersistenceMsg::Create { entry, respond_to } => {
                // 1_745_193_600 is the elapse from epoch generate for 2025-4-21, + 1234 ns as seed
                let ts = Timestamp::from_unix(NoContext, 1_745_193_600, 1234);
                let uuid = Uuid::new_v7(ts);

                match entry {
                    Entry::Node(val) => {
                        println!("Dump node entry {uuid}: '{val}'");
                    }
                    Entry::Task { name } => {
                        println!("Dump task entry {uuid}: '{name}'");
                    }
                    Entry::Edge { src, legend, dst } => {
                        if let Some(legend) = legend {
                            println!("Dump edge entry {uuid}: {src} --{legend}--> {dst}");
                        } else {
                            println!("Dump edge entry {uuid}: {src} --> {dst}");
                        }
                    }
                }

                let _ = respond_to.send(uuid);
            }
            PersistenceMsg::Update => todo!(),
            PersistenceMsg::Get => todo!(),
            PersistenceMsg::Delete => todo!(),
        }
    }
}

#[derive(Debug)]
pub struct FilePersistence {
    path: PathBuf,
    receiver: mpsc::Receiver<PersistenceMsg>,
}

impl FilePersistence {
    /// # Panics
    /// raise if unable to get current directory.
    #[must_use]
    pub fn new(receiver: mpsc::Receiver<PersistenceMsg>) -> Self {
        let path = std::env::current_dir().expect("unable to get current dir");
        let path = path.join("provenance_dump.csv");
        if !path.is_file() {
            let mut fh = std::fs::File::create(&path).expect("unable to create the file");
            fh.write_all("uuid, typ, entry\n".as_bytes())
                .expect("unable to write header of file");
        }
        FilePersistence { path, receiver }
    }
}

impl PersistenceActor for FilePersistence {
    async fn receive(&mut self) -> Option<PersistenceMsg> {
        self.receiver.recv().await
    }

    fn handle_message(&mut self, msg: PersistenceMsg) {
        match msg {
            PersistenceMsg::Create { entry, respond_to } => {
                // 1_745_193_600 is the elapse from epoch generate for 2025-4-21, + 1234 ns as seed
                let ts = Timestamp::from_unix(NoContext, 1_745_193_600, 1234);
                let uuid = Uuid::new_v7(ts);

                let row = match entry {
                    Entry::Node(val) => {
                        let value_str = serde_json::to_string(&val).expect("value serialized fail");
                        format!("{uuid}, node, {value_str}\n")
                    }
                    Entry::Task { name } => {
                        format!("{uuid}, task, {name}\n")
                    }
                    Entry::Edge { src, legend, dst } => {
                        if let Some(legend) = legend {
                            format!("{uuid}, edge, {src} --{legend}--> {dst}\n")
                        } else {
                            format!("{uuid}, edge, {src} --> {dst}\n")
                        }
                    }
                };

                let fh = fs::File::options()
                    .append(true)
                    .open(&self.path)
                    .expect("unable to open to append entry");
                let mut fh = BufWriter::new(fh);
                fh.write_all(row.as_bytes())
                    .expect("unable to append to the persistence");

                let _ = respond_to.send(uuid);
            }
            PersistenceMsg::Update => todo!(),
            PersistenceMsg::Get => todo!(),
            PersistenceMsg::Delete => todo!(),
        }
    }
}

async fn run_persistence_actor<A>(mut actor: A)
where
    A: PersistenceActor,
{
    while let Some(msg) = actor.receive().await {
        actor.handle_message(msg);
    }
}
