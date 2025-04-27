use std::sync::Arc;
use tokio::{
    sync::{mpsc, Notify},
    task::{spawn_local, JoinHandle},
};

use crate::error::Error;

#[derive(Debug)]
pub enum HandlerEvent {
    Kill,
    Pause,
}

pub trait State: Clone {
    // the initial state
    fn init() -> Self;
    fn is_done(&self) -> bool;
    fn is_paused(&self) -> bool;
}

pub trait Process<S: State> {
    // XXX: can I make this as similar as `Future` trait? by making `advance` method similar as
    // `poll` and return a ready that resolved to output and pending as `Pending<State>`?
    type Output;

    fn state(&self) -> &S;
    fn transition_to(&mut self, state: S);
    fn is_done(&self) -> bool {
        self.state().is_done()
    }
    fn is_paused(&self) -> bool {
        self.state().is_paused()
    }
    fn output(&self) -> Option<Self::Output>;
    fn kill(&mut self) -> impl std::future::Future<Output = S>;
    fn advance(&mut self) -> impl std::future::Future<Output = S>;

    // XXX: pause is a bit specific for resource related process, consider to make
    // it plausible by dyn check the trait implementation.
    fn pause(&mut self) -> impl std::future::Future<Output = S>;
}

#[derive(Debug)]
pub struct ProcessHandler<S>
where
    S: Clone,
{
    event_sender: mpsc::Sender<HandlerEvent>,
    nudge_sender: mpsc::Sender<()>,
    state_receiver: tokio::sync::watch::Receiver<S>,
    resume_notifier: Arc<Notify>,
}

impl<S> ProcessHandler<S>
where
    S: State,
{
    /// Attempts to send a nudge signal to advance the process.
    ///
    /// This function performs a non-blocking send operation on the `nudge`
    /// channel. The channel has a buffer size of 1, meaning it can hold
    /// only one notification at a time. If a notification is already in
    /// the queue, the function will return an error indicating that the
    /// channel is full.
    ///
    /// # Returns
    ///
    /// return  `Ok(())` if the nudge signal was successfully sent.
    ///
    /// # Errors
    ///
    /// return  `Err(mpsc::error::TrySendError<()>)` if the channel is full,
    ///   meaning a notification is already pending.
    // XXX: own error type
    pub fn try_nudge(&self) -> Result<(), mpsc::error::TrySendError<()>> {
        self.nudge_sender.try_send(())
    }

    pub async fn nudge(&self) {
        let _ = self.nudge_sender.send(()).await;
    }

    /// Sends a kill signal to terminate the process.
    ///
    /// This method attempts to send an ``HandlerEvent::Kill`` signal to the event channel,
    /// requesting the process to shut down gracefully. If the event channel is closed,
    /// the function returns an [`Error::EventChannelClosed`] error.
    ///
    /// # Errors
    ///
    /// Returns [`Error::EventChannelClosed`] if the event channel is closed
    /// and the message cannot be sent.
    pub async fn kill(&self) -> Result<(), Error> {
        // try to resume first to break the pauser
        self.resume_notifier.notify_one();

        self.event_sender
            .send(HandlerEvent::Kill)
            .await
            .map_err(|send_error| Error::EventChannelClosed(send_error.0))
    }

    /// Sends a pause signal to terminate the process.
    ///
    /// This method attempts to send an ``HandlerEvent::Pause`` message to the event channel,
    /// requesting the process to pause and wait for a resume signal. If the event channel
    /// is closed, the function returns an [`Error::EventChannelClosed`] error.
    ///
    /// # Errors
    ///
    /// Returns [`Error::EventChannelClosed`] if the event channel is closed
    /// and the message cannot be sent.
    pub async fn pause(&self) -> Result<(), Error> {
        self.event_sender
            .send(HandlerEvent::Pause)
            .await
            .map_err(|send_error| Error::EventChannelClosed(send_error.0))
    }

    pub fn resume(&self) {
        self.resume_notifier.notify_one();
    }

    #[must_use]
    pub fn state(&self) -> S {
        self.state_receiver.borrow().clone()
    }

    // mostly for debug purpose:
    // inspect return the state of current process
    // I made this an async call because it designed for only used in Step mode, mostly for debug
    // and test.
    // In the production environment, it is meaningless to check the state of a process since it is
    // in a runtime and will unpredictly advanced to an unknown state.
    pub async fn wait_for_state_change(&mut self) -> Option<S> {
        if self.state_receiver.changed().await.is_ok() {
            Some(self.state_receiver.borrow().clone())
        } else {
            // channel closed after proc is done
            None
        }
    }

    #[must_use]
    pub fn is_done(&self) -> bool {
        self.state_receiver.borrow().is_done()
    }
}

pub enum DriveMode {
    FireAndForget,
    Step,
}

// launch the process, `drive_mode` to set if the process start and run to end or it needs to
// be drived for every step through a signal.
//
// It uses `spawn_local` of `LocalSet`, unlike the free function [`spawn_local`], this method is used to
// spawn local tasks when the `LocalSet` is *not* running.
// The provided future will start running once the `LocalSet` is next started, even if
// I don't await the returned `JoinHandle`.
//
// This task is guaranteed to be run on the current thread rather than be able to be send to other threads.
// This disable the work steal and confine the process run in one thread to avoid complexity on
// trait bound and unnecessary environment capture of Process which can be large data chuck.
// Moreover, ensure it is not crossing the threads make the input/output do not need to be `Send`.
pub fn launch<S, P, O>(
    mut proc: P,
    drive_mode: DriveMode,
) -> (JoinHandle<Option<O>>, ProcessHandler<S>)
where
    S: State + 'static,
    O: 'static,
    P: Process<S, Output = O> + 'static,
{
    // channel for events/nudge and for send state info out
    let (event_tx, mut event_rx) = mpsc::channel::<HandlerEvent>(10);
    let (nudge_tx, mut nudge_rx) = mpsc::channel::<()>(1);
    let (state_tx, state_rx) = tokio::sync::watch::channel(S::init());
    // notifier to resume
    let resume_notifier = Arc::new(Notify::new());
    let resume_notifier_cloned = resume_notifier.clone();

    let join_handle = spawn_local(async move {
        // await for launch trigger in fire and forget mode, loop will continue to the end
        if matches!(drive_mode, DriveMode::FireAndForget) {
            let _ = nudge_rx.recv().await;
        }
        loop {
            if !proc.is_done() && matches!(drive_mode, DriveMode::Step) {
                let _ = nudge_rx.recv().await;
            }
            while let Ok(event) = event_rx.try_recv() {
                match event {
                    HandlerEvent::Kill => {
                        let next_state = proc.kill().await;
                        let _prev_state = state_tx.send_replace(next_state);
                    }
                    HandlerEvent::Pause => {
                        let next_state = proc.pause().await;
                        let _prev_state = state_tx.send_replace(next_state);
                    }
                }
            }
            if proc.is_done() {
                // drop receiver so no event signal can send.
                drop(event_rx);
                break;
            }
            if proc.is_paused() {
                // TODO: check when se/de is there recreate process can jump to paused state.

                // block until pause breaker notification arrived.
                resume_notifier_cloned.notified().await;
            }
            let next_state = proc.advance().await;
            let _ = state_tx.send_replace(next_state);
            // TODO: tracing log
        }
        proc.output()
    });
    let comm = ProcessHandler {
        event_sender: event_tx,
        nudge_sender: nudge_tx,
        state_receiver: state_rx,
        resume_notifier,
    };

    (join_handle, comm)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[derive(PartialEq, Clone, Debug)]
    enum DummyState {
        Begin,
        End,
    }

    #[derive(Debug)]
    pub enum Event {
        Run,
        Pause,
        Terminate,
    }

    impl State for DummyState {
        fn init() -> Self {
            DummyState::Begin
        }
        fn is_done(&self) -> bool {
            self == &DummyState::End
        }

        // never paused
        fn is_paused(&self) -> bool {
            false
        }
    }

    impl DummyState {
        fn next(&self, event: Event) -> DummyState {
            match (&self, event) {
                (DummyState::Begin, Event::Run | Event::Terminate) => DummyState::End,
                (s, e) => {
                    panic!("Wrong state, event combination: state - {s:#?}, event - {e:#?}")
                }
            }
        }
    }

    #[derive(Debug)]
    struct AddProc {
        state: DummyState,
        inp1: i32,
        inp2: i32,
        output: Option<i32>,
    }

    impl AddProc {
        fn execute(&mut self) {
            self.output = Some(self.inp1 + self.inp2);
        }
    }

    impl Process<DummyState> for AddProc {
        type Output = i32;

        fn state(&self) -> &DummyState {
            &self.state
        }
        fn transition_to(&mut self, state: DummyState) {
            self.state = state;
        }
        fn is_done(&self) -> bool {
            self.state().is_done()
        }
        fn is_paused(&self) -> bool {
            self.state().is_paused()
        }
        fn output(&self) -> Option<i32> {
            self.output
        }
        async fn kill(&mut self) -> DummyState {
            self.state = self.state.next(Event::Terminate);
            self.state.clone()
        }
        async fn pause(&mut self) -> DummyState {
            self.state = self.state.next(Event::Pause);
            self.state.clone()
        }
        async fn advance(&mut self) -> DummyState {
            self.state = match self.state {
                DummyState::Begin => {
                    self.execute();
                    println!(
                        "Computed {} + {} = {}",
                        self.inp1,
                        self.inp2,
                        self.output.unwrap()
                    );
                    self.state.next(Event::Run)
                }
                DummyState::End => unreachable!(),
            };
            self.state.clone()
        }
    }

    impl AddProc {
        fn new(inp1: i32, inp2: i32) -> AddProc {
            AddProc {
                state: DummyState::Begin,
                inp1,
                inp2,
                output: None,
            }
        }
    }

    #[tokio::test]
    async fn test_add_proc() {
        #[derive(Debug)]
        struct AddTask {
            input: (i32, i32),
            output: Option<i32>,
            proc: Option<AddProc>,
        }

        impl AddTask {
            fn new(inp1: i32, inp2: i32) -> Self {
                let input = (inp1, inp2);
                let proc = Some(AddProc::new(input.0, input.1));
                AddTask {
                    input,
                    output: None,
                    proc,
                }
            }
        }

        let mut task = AddTask::new(6, 4);
        let proc = task.proc.take().unwrap();
        let local = tokio::task::LocalSet::new();
        let (joiner, handler) = launch(proc, DriveMode::FireAndForget);

        local
            .run_until(async {
                assert!(handler.try_nudge().is_ok());
                task.output = joiner.await.unwrap();
            })
            .await;

        assert!(handler.is_done());
        assert_eq!(handler.state(), DummyState::End);
        assert_eq!(task.input, (6, 4));
        assert_eq!(task.output, Some(6 + 4));
    }
}
