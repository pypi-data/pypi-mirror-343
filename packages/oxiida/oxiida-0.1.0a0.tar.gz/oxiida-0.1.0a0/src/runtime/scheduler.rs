use crate::runtime::core::{Process, State};
use std::time::Duration;

#[derive(Debug, PartialEq, Clone)]
struct MetaData {
    name: String,
}

impl MetaData {
    fn new(name: &str) -> Self {
        MetaData { name: name.into() }
    }
}

#[derive(Debug)]
pub enum Event {
    Run,
    Pause,
    Resume,

    // reserved exit code
    // 9 for kill to sync with Linux SIGKILL
    // 0 for finish ok
    Terminate(i32),
}

/// These are sub-states of waiting/running state
/// They are used to route between ``run_fn`` and ``wait_fn`` for different communication with the
/// resources.
/// The op should be the most atomic operations with remote, which means they are idempodent.
/// Between the ops, are where the checkpoint stored.
#[derive(Debug, PartialEq, Clone)]
enum Action {
    // Init and prepare the inputs
    Init,
    // upload the init inputs to remote
    Upload,
    // submit the job by interact with remote
    Submit,
    // check if the remote state updated
    Update,
    // Retrieve the data when finished
    Retrieve,
    // Parsing the output from retrieved data
    Parse,
}

#[derive(Debug, PartialEq, Clone)]
enum RemoteJobState<A> {
    Created,
    Running { action: A },
    Waiting { action: A },
    Paused { prev: Box<RemoteJobState<A>> },
    Finished,
    Killed,
    Excepted(String),
}

impl State for RemoteJobState<Action> {
    fn init() -> Self {
        RemoteJobState::Created
    }
    fn is_done(&self) -> bool {
        matches!(
            self,
            RemoteJobState::Finished | RemoteJobState::Excepted(..) | RemoteJobState::Killed
        )
    }
    fn is_paused(&self) -> bool {
        matches!(self, RemoteJobState::Paused { .. })
    }
}

impl RemoteJobState<Action> {
    fn next(self, event: Event) -> RemoteJobState<Action> {
        // no clone except paused, thus zero-cost state transition for other states.
        match (self, event) {
            (RemoteJobState::Created, Event::Run) => RemoteJobState::Running {
                action: Action::Init,
            },
            #[allow(clippy::match_same_arms)]
            (RemoteJobState::Created, Event::Terminate(9)) => RemoteJobState::Killed,
            (RemoteJobState::Created, Event::Pause) => {
                eprintln!("pause on create state, nothing happend");
                RemoteJobState::Created
            }
            (RemoteJobState::Running { action }, Event::Pause) => RemoteJobState::Paused {
                prev: Box::new(RemoteJobState::Running { action }),
            },
            (RemoteJobState::Waiting { action }, Event::Pause) => RemoteJobState::Paused {
                prev: Box::new(RemoteJobState::Waiting { action }),
            },
            (RemoteJobState::Paused { prev }, Event::Resume) => *prev,
            (
                RemoteJobState::Running { .. } | RemoteJobState::Paused { .. },
                Event::Terminate(9),
            ) => RemoteJobState::Killed,
            (s, e) => RemoteJobState::Excepted(format!(
                "Wrong state, event combination: state - {s:#?}, event - {e:#?}"
            )),
        }
    }
}

#[derive(Debug, Clone)]
struct Output {}

#[derive(Debug)]
pub struct SchedulerProcess<I, O> {
    state: RemoteJobState<Action>,
    meta: Option<MetaData>,
    input: I,
    output: Option<O>,
}

impl<I, O> Process<RemoteJobState<Action>> for SchedulerProcess<I, O>
where
    O: Clone,
{
    type Output = O;

    fn state(&self) -> &RemoteJobState<Action> {
        &self.state
    }
    fn transition_to(&mut self, state: RemoteJobState<Action>) {
        self.state = state;
    }

    // TODO: state switch + cancellation operations should be triggered through handler
    // Besides, should not contain more complex logic.
    // The kill will skip following states and arrive to the final killed state
    // Should also mimic tokio API to have a try_kill that is non-blocking sync call.
    async fn kill(&mut self) -> RemoteJobState<Action> {
        self.state = self.state.clone().next(Event::Terminate(9));
        self.state.clone()
    }

    // TODO: pause looks like kill, it cancel the current operations (if sync, it wait until
    // finish, if async, it send a cancel ??? is this consist with each other, think monkey think)
    // The the different from kill is pause will jump to pause state and can resume instead of skip
    // to the final state.
    async fn pause(&mut self) -> RemoteJobState<Action> {
        self.state = self.state.clone().next(Event::Pause);
        self.state.clone()
    }
    async fn advance(&mut self) -> RemoteJobState<Action> {
        self.state = match self.state {
            RemoteJobState::Created => self.state.clone().next(Event::Run),
            RemoteJobState::Running { .. } => self.run_fn(),
            RemoteJobState::Waiting { .. } => self.wait_fn().await,
            RemoteJobState::Paused { .. } => self.state.clone().next(Event::Resume),
            // done states cannot be advanced
            RemoteJobState::Killed | RemoteJobState::Finished | RemoteJobState::Excepted(_) => {
                unreachable!()
            }
        };
        self.state.clone()
    }

    fn output(&self) -> Option<Self::Output> {
        self.output.clone()
    }
}

impl<I, O> SchedulerProcess<I, O> {
    pub fn new(name: &str, input: I) -> Self {
        SchedulerProcess {
            state: RemoteJobState::Created,
            meta: Some(MetaData::new(name)),
            input,
            output: None,
        }
    }
}

impl<I, O> SchedulerProcess<I, O> {
    fn run_fn(&mut self) -> RemoteJobState<Action> {
        // execute in playing state
        println!("I am run_fn");
        match &self.state {
            RemoteJobState::Running {
                action: Action::Init,
            } => {
                // TODO: ?
                RemoteJobState::Waiting {
                    action: Action::Upload,
                }
            }
            RemoteJobState::Running {
                action: Action::Parse,
            } => {
                println!("placeholder: if parsing okay, complete");
                RemoteJobState::Finished
            }
            _ => unreachable!(),
        }
    }

    async fn wait_fn(&mut self) -> RemoteJobState<Action> {
        match &self.state {
            RemoteJobState::Waiting {
                action: Action::Upload,
            } => {
                // let sandbox_path = self.input.generate_files();

                tokio::time::sleep(Duration::from_millis(20)).await;
                RemoteJobState::Waiting {
                    action: Action::Submit,
                }
            }
            RemoteJobState::Waiting {
                action: Action::Submit,
            } => {
                println!("placeholder: remote submit");
                RemoteJobState::Waiting {
                    action: Action::Update,
                }
            }
            // Action::Update => {
            //     // TODO: some tokio timeout functionality implemented here.
            //     println!("placeholder: remote submit");
            //     self.action = Action::Update;
            //     RemoteJobState::Waiting
            // }
            RemoteJobState::Waiting {
                action: Action::Update,
            } => {
                println!("placeholder: remote update");
                RemoteJobState::Waiting {
                    action: Action::Retrieve,
                }
            }
            RemoteJobState::Waiting {
                action: Action::Retrieve,
            } => {
                println!("placeholder: remote retrive");
                RemoteJobState::Running {
                    action: Action::Parse,
                }
            }
            _ => unreachable!(),
        }
    }
}

#[derive(Debug)]
struct SchedulerTask<I, O> {
    proc: Option<SchedulerProcess<I, O>>,
    output: Option<O>,
}

impl<I, O> SchedulerTask<I, O> {
    fn new(name: &str, input: I) -> Self {
        SchedulerTask {
            proc: Some(SchedulerProcess::new(name, input)),
            output: None,
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::{
        error::Error,
        runtime::core::{launch, DriveMode, HandlerEvent},
    };

    use super::*;

    struct Input;

    #[derive(Clone)]
    struct Output;

    #[tokio::test(start_paused = true)]
    async fn test_fire_and_forget() {
        let local = tokio::task::LocalSet::new();
        let mut task = SchedulerTask::<Input, Output>::new("The Beatles - Julia", Input);
        let proc = task.proc.take().unwrap();

        local
            .run_until(async {
                let (joiner, handler) = launch(&local, proc, DriveMode::FireAndForget);
                assert!(handler.try_nudge().is_ok());
                task.output = joiner.await.unwrap();
            })
            .await;
    }

    #[tokio::test(start_paused = true)]
    async fn test_round_trip() {
        let local = tokio::task::LocalSet::new();
        let mut task = SchedulerTask::<Input, Output>::new("The Beatles - Julia", Input);
        let proc = task.proc.take().unwrap();

        local
            .run_until(async {
                let (joiner, mut handler) = launch(&local, proc, DriveMode::Step);

                // The sequence of states we expect to see, in order:
                let expected_states = [
                    RemoteJobState::Running {
                        action: Action::Init,
                    },
                    RemoteJobState::Waiting {
                        action: Action::Upload,
                    },
                    RemoteJobState::Waiting {
                        action: Action::Submit,
                    },
                    RemoteJobState::Waiting {
                        action: Action::Update,
                    },
                    RemoteJobState::Waiting {
                        action: Action::Retrieve,
                    },
                    RemoteJobState::Running {
                        action: Action::Parse,
                    },
                    RemoteJobState::Finished,
                ];

                for expected in expected_states {
                    assert!(handler.try_nudge().is_ok());
                    let new_state = handler.wait_for_state_change().await;
                    // handy; since State` + `Action` implement `Debug` + `PartialEq`.
                    assert_eq!(new_state.as_ref(), Some(&expected));
                }

                // After all states are exhausted, we expect None
                let new_state = handler.wait_for_state_change().await;
                assert!(new_state.is_none());

                task.output = joiner.await.unwrap();
            })
            .await;
    }

    #[tokio::test]
    async fn test_create_kill() {
        let local = tokio::task::LocalSet::new();
        let mut task = SchedulerTask::<Input, Output>::new("The Beatles - Julia", Input);
        let proc = task.proc.take().unwrap();

        local
            .run_until(async {
                let (joiner, mut handler) = launch(&local, proc, DriveMode::Step);
                assert!(handler.try_nudge().is_ok());
                assert!(handler.kill().await.is_ok());
                let new_state = handler.wait_for_state_change().await;
                assert_eq!(new_state.as_ref(), Some(&RemoteJobState::Killed));

                task.output = joiner.await.unwrap();
            })
            .await;
    }

    #[tokio::test(start_paused = true)]
    async fn test_pause_on_create() {
        // pause on create, nothing happened, but firing a log
        let local = tokio::task::LocalSet::new();
        let mut task = SchedulerTask::<Input, Output>::new("The Beatles - Julia", Input);
        let proc = task.proc.take().unwrap();

        local
            .run_until(async {
                let (joiner, mut handler) = launch(&local, proc, DriveMode::Step);

                assert!(handler.pause().await.is_ok());
                // TODO: test log fires

                assert!(handler.try_nudge().is_ok());

                assert!(handler.pause().await.is_ok());
                // TODO: test log fires

                let new_state = handler.wait_for_state_change().await;

                assert_eq!(
                    new_state.as_ref(),
                    Some(&RemoteJobState::Running {
                        action: Action::Init
                    })
                );

                while !handler.is_done() {
                    // The equavalent call is:
                    // ```
                    // handler.try_nudge();
                    // tokio::task::yield_now().await;
                    // ```
                    // The blocking try_nudge introduce a tight loop that block the thread.

                    handler.nudge().await;
                }

                task.output = joiner.await.unwrap();
            })
            .await;
    }

    #[tokio::test(start_paused = true)]
    async fn test_pause_and_resume() {
        let local = tokio::task::LocalSet::new();
        let mut task = SchedulerTask::<Input, Output>::new("The Beatles - Julia", Input);
        let proc = task.proc.take().unwrap();

        local
            .run_until(async {
                let (joiner, mut handler) = launch(&local, proc, DriveMode::Step);

                assert!(handler.try_nudge().is_ok());
                let new_state = handler.wait_for_state_change().await;
                assert_eq!(
                    new_state.as_ref(),
                    Some(&RemoteJobState::Running {
                        action: Action::Init
                    })
                );
                // simulate the case when at running state get a pause signal
                let _ = handler.pause().await;
                assert!(handler.try_nudge().is_ok());
                let new_state = handler.wait_for_state_change().await;
                assert_eq!(
                    new_state.as_ref(),
                    Some(&RemoteJobState::Paused {
                        prev: Box::new(RemoteJobState::Running {
                            action: Action::Init
                        })
                    })
                );

                // after pause, nudge signal in queue cannot be consumed
                assert!(handler.try_nudge().is_ok());
                assert!(handler.try_nudge().is_err());
                assert!(handler.try_nudge().is_err());
                assert!(handler.try_nudge().is_err());
                assert!(handler.try_nudge().is_err());

                // resume
                handler.resume();

                let new_state = handler.wait_for_state_change().await;
                // depend on whether the left try_nudge signal arrived, the state is unsure.
                // But since it is resumed so must not a paused state.
                assert_ne!(
                    new_state.as_ref(),
                    Some(&RemoteJobState::Paused {
                        prev: Box::new(RemoteJobState::Running {
                            action: Action::Init
                        })
                    })
                );

                while !handler.is_done() {
                    handler.nudge().await;
                }

                task.output = joiner.await.unwrap();
            })
            .await;
    }

    #[tokio::test]
    async fn test_kill_pause_done_state() {
        let local = tokio::task::LocalSet::new();
        let mut task = SchedulerTask::<Input, Output>::new("The Beatles - Julia", Input);
        let proc = task.proc.take().unwrap();

        local
            .run_until(async {
                let (joiner, mut handler) = launch(&local, proc, DriveMode::Step);
                assert!(handler.try_nudge().is_ok());
                let _ = handler.kill().await;
                let new_state = handler.wait_for_state_change().await;
                assert_eq!(new_state.as_ref(), Some(&RemoteJobState::Killed));

                let got = handler.kill().await;
                assert!(matches!(
                    got,
                    Err(Error::EventChannelClosed(HandlerEvent::Kill))
                ));

                let got = handler.pause().await;
                assert!(matches!(
                    got,
                    Err(Error::EventChannelClosed(HandlerEvent::Pause))
                ));

                task.output = joiner.await.unwrap();
            })
            .await;
    }
}
