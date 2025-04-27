#![allow(clippy::redundant_closure_for_method_calls, clippy::match_same_arms)]

/*
Shell cmd run through ``tokio::process`` in async manner, thus require --features process as dep.
Therefore the format of construct a command has the same limitation (and caveats) as ``tokio::process::Command``.
The command and args are passed as str.
See https://docs.rs/tokio/latest/tokio/process/struct.Command.html.
XXX: this information should goto oxiida doc as well lead user on how and why need double quotes for the command.
*/
use nix::sys::signal::Signal::SIGCONT;
use nix::sys::{self, signal::Signal::SIGSTOP};
use nix::unistd::Pid;
use std::collections::HashMap;
use std::ffi::{OsStr, OsString};
use std::io;
use std::process::ExitStatus;
use std::process::Stdio;
use tokio::io::AsyncWriteExt;
use tokio::{io::AsyncReadExt, process::Child};

use crate::lang::ast;
use crate::runtime::core::{Process, State};

#[derive(PartialEq, Clone, Debug)]
pub enum ShellState {
    Created,
    Running,
    Waiting,
    Paused,
    Finished,
    Killed,
    // TODO: make it a Cow to be cheaper
    Failed(i32, String),
}

#[derive(Debug)]
pub enum Event {
    Continue,
    Pause,
    Resume,
    Kill,
    Finish,
    Fail(i32),
}

impl State for ShellState {
    fn init() -> Self {
        ShellState::Created
    }
    fn is_done(&self) -> bool {
        matches!(
            self,
            ShellState::Finished | ShellState::Killed | ShellState::Failed(..)
        )
    }

    fn is_paused(&self) -> bool {
        matches!(self, ShellState::Paused)
    }
}

impl ShellState {
    fn next(&mut self, event: Event) -> ShellState {
        match (self, event) {
            (ShellState::Created, Event::Continue) => ShellState::Running,
            (ShellState::Created, Event::Pause) => {
                eprintln!("pause on create state, nothing happend");
                ShellState::Created
            }
            (ShellState::Running, Event::Pause) => ShellState::Paused,
            (ShellState::Waiting, Event::Pause) => ShellState::Paused,
            (ShellState::Paused, Event::Resume) => ShellState::Waiting,
            (ShellState::Running, Event::Continue) => ShellState::Waiting,
            (ShellState::Waiting, Event::Finish) => ShellState::Finished,
            (_, Event::Kill) => ShellState::Killed,
            (s, e) => {
                panic!("Invalid state transition: state - {s:?}, event - {e:?}")
            }
        }
    }

    #[allow(clippy::needless_pass_by_value)]
    fn fast_fail(&mut self, event: Event, err: Box<dyn std::error::Error>) -> ShellState {
        match (self, event) {
            (ShellState::Waiting | ShellState::Running, Event::Fail(code)) => {
                ShellState::Failed(code, err.to_string())
            }
            (s, e) => {
                panic!("Invalid fast fail termination: state - {s:?}, event - {e:?}")
            }
        }
    }
}

#[derive(Debug)]
pub struct ShellProcess {
    state: ShellState,
    cmd: OsString,
    cmd_args: Vec<OsString>,
    stdin: Option<OsString>,

    // when the cmd construct and running, this is the handler.
    child: Option<Child>,
    output: Option<std::process::Output>,
}

impl Process<ShellState> for ShellProcess {
    type Output = std::process::Output;

    fn state(&self) -> &ShellState {
        &self.state
    }
    fn transition_to(&mut self, state: ShellState) {
        self.state = state;
    }
    fn is_done(&self) -> bool {
        self.state().is_done()
    }
    fn is_paused(&self) -> bool {
        self.state().is_paused()
    }
    // TODO: error handle propagate
    async fn kill(&mut self) -> ShellState {
        let child = self.child.as_mut().expect("child process not exist");
        // XXX: here to write stream from child to process stdout the code is duplicate as `advance`
        // since they share the same logic, can consider put it in one place.
        child.start_kill().expect("kill failed");

        // Take stdout and stderr to read after waiting
        let stdout = child.stdout.take();
        let stderr = child.stderr.take();

        // Now, fully read stdout and stderr into buffer
        let mut stdout_buf = Vec::new();
        let mut stderr_buf = Vec::new();

        if let Some(mut out) = stdout {
            let _ = out.read_to_end(&mut stdout_buf).await;
        }

        if let Some(mut err) = stderr {
            let _ = err.read_to_end(&mut stderr_buf).await;
        }
        match child.wait().await {
            Ok(exit_state) => {
                self.output = Some(std::process::Output {
                    stdout: stdout_buf,
                    stderr: stderr_buf,
                    status: exit_state,
                });
                self.state = self.state.next(Event::Kill);
                self.state.clone()
            }
            Err(err) => self.state.fast_fail(Event::Fail(1), Box::new(err)),
        }
    }
    // TODO: error handle propagate
    async fn pause(&mut self) -> ShellState {
        // send SIGSTOP (19)
        if let Some(pid) = self.child.as_ref().and_then(|child| child.id()) {
            #[allow(clippy::cast_possible_wrap)]
            let _ = sys::signal::kill(Pid::from_raw(pid as i32), SIGSTOP);
        }
        self.state = self.state.next(Event::Pause);
        self.state.clone()
    }
    async fn advance(&mut self) -> ShellState {
        self.state = match self.state {
            ShellState::Created => self.state.next(Event::Continue),
            ShellState::Running => {
                // construct cmd and spawn the child handler.
                let mut cmd = tokio::process::Command::new(&self.cmd);

                // read args and capture stdout/stderr
                cmd.args(&self.cmd_args);
                if self.stdin.is_some() {
                    cmd.stdin(Stdio::piped());
                }
                cmd.stdout(Stdio::piped()).stderr(Stdio::piped());

                // spawn and moving to waiting
                match cmd.spawn() {
                    Ok(mut child) => {
                        // capture stdin, essential to cacll take() to move stdin out from child so
                        // it can be dropped.
                        // https://docs.rs/tokio/latest/tokio/process/struct.Child.html?utm_source=chatgpt.com#structfield.stdin
                        if let (Some(input), Some(mut stdin)) = (&self.stdin, child.stdin.take()) {
                            stdin
                                .write_all(input.as_encoded_bytes())
                                .await
                                .expect("unable to write to stdin");
                            stdin
                                .shutdown()
                                .await
                                .expect("unable to shutdown stdin channel");
                        }

                        // First, wait for the child process to complete
                        self.child = Some(child);

                        // transition to waiting state for waiting for finish.
                        self.state.next(Event::Continue)
                    }
                    Err(err) => self.state.fast_fail(Event::Fail(1), Box::new(err)),
                }
            }
            ShellState::Waiting => {
                let child = self.child.as_mut().expect("child process not exist");
                // Take stdout and stderr to read after waiting
                let stdout = child.stdout.take();
                let stderr = child.stderr.take();

                // Now, fully read stdout and stderr into buffer
                let mut stdout_buf = Vec::new();
                let mut stderr_buf = Vec::new();

                if let Some(mut out) = stdout {
                    let _ = out.read_to_end(&mut stdout_buf).await;
                }

                if let Some(mut err) = stderr {
                    let _ = err.read_to_end(&mut stderr_buf).await;
                }

                match child.wait().await {
                    Ok(exit_state) => {
                        self.output = Some(std::process::Output {
                            stdout: stdout_buf,
                            stderr: stderr_buf,
                            status: exit_state,
                        });

                        // state transitions
                        if exit_state.success() {
                            self.state.next(Event::Finish)
                        } else {
                            self.state.fast_fail(
                                Event::Fail(1),
                                Box::new(io::Error::new(
                                    io::ErrorKind::Other,
                                    format!(
                                        "command execution failed - {:?}",
                                        exit_state.to_string()
                                    ),
                                )),
                            )
                        }
                    }
                    Err(err) => self.state.fast_fail(Event::Fail(1), Box::new(err)),
                }
            }
            ShellState::Paused => {
                // If it is paused, and get chance to advance, means it is resuming.
                // resume by sending a `SIGCONT` signal.
                if let Some(pid) = self.child.as_ref().and_then(|child| child.id()) {
                    #[allow(clippy::cast_possible_wrap)]
                    let _ = sys::signal::kill(Pid::from_raw(pid as i32), SIGCONT);
                }
                self.state.next(Event::Resume)
            }
            ShellState::Killed | ShellState::Finished | ShellState::Failed(..) => {
                unreachable!()
            }
        };
        self.state.clone()
    }

    fn output(&self) -> Option<Self::Output> {
        self.output.clone()
    }
}

// XXX: the name "Output" is very confuse and easy to mix up with process one and
// std::process::Output. Maybe `ShellResult` can be better.
#[derive(Debug, Clone)]
pub struct Output {
    pub status: ExitStatus,
    pub stdout: Vec<u8>,
    pub stderr: Vec<u8>,
}

impl From<Output> for ast::Value {
    fn from(value: Output) -> Self {
        let mut dict = HashMap::new();
        dict.insert(
            "status".into(),
            ast::Value::String(value.status.to_string()),
        );
        dict.insert(
            "stdout".into(),
            ast::Value::String(String::from_utf8_lossy(&value.stdout).to_string()),
        );
        dict.insert(
            "stderr".into(),
            ast::Value::String(String::from_utf8_lossy(&value.stderr).to_string()),
        );
        ast::Value::Dict(dict)
    }
}

impl Output {
    #[must_use]
    pub fn from(pout: std::process::Output) -> Self {
        // TODO: a bit redundant for the process Output, prototype to show how to have
        // customized output format.
        //
        // although the name is borrowed from From trait, it is not impl of From trait,
        // since here the convention usually cause the data lossness.
        Output {
            status: pout.status,
            stdout: pout.stdout,
            stderr: pout.stderr,
        }
    }
}

#[derive(Debug)]
pub struct ShellTask {
    pub cmd_literal: String,
    pub output: Option<Output>,
    pub proc: Option<ShellProcess>,
}

impl std::fmt::Display for ShellTask {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.cmd_literal)
    }
}

impl ShellTask {
    pub fn new<S, I>(cmd: S, cmd_args: I, stdin: Option<S>) -> Self
    where
        I: IntoIterator<Item = S>,
        S: AsRef<OsStr>,
    {
        let cmd_args: Vec<_> = cmd_args.into_iter().map(|ref s| s.into()).collect();
        let stdin = stdin.map(|s| (&s).into());

        let proc = Some(ShellProcess {
            state: ShellState::Created,
            cmd: (&cmd).into(),
            cmd_args: cmd_args.clone(),
            stdin: stdin.clone(),
            child: None,
            output: None,
        });

        // TODO: optimizing performance, too many heap allocation
        let cmd_literal = cmd.as_ref().to_string_lossy().to_string();
        let args_literal = cmd_args
            .iter()
            .map(|arg| arg.to_string_lossy())
            .collect::<Vec<_>>()
            .join(" ");
        let cmd_literal = [cmd_literal, args_literal].join(" ");
        let cmd_literal = if let Some(stdin) = stdin {
            let stdin = stdin.to_string_lossy().to_string();
            [cmd_literal, stdin].join(" <-| ")
        } else {
            cmd_literal
        };

        ShellTask {
            cmd_literal,
            output: None,
            proc,
        }
    }
}

#[cfg(test)]
mod tests {
    use std::os::unix::process::ExitStatusExt;
    use tokio::time::Instant;

    use crate::runtime::core::{launch, DriveMode};
    // use nix::sys::wait::{waitpid, WaitPidFlag, WaitStatus};
    // use nix::unistd::Pid;

    use super::*;

    #[tokio::test]
    async fn test_run_cmd_finish() {
        // test run `echo "thanks rust!"` command and write result to output of process.
        let mut task = ShellTask::new("echo", ["thanks rust!"], None);
        let proc = task.proc.take().unwrap();
        let local = tokio::task::LocalSet::new();
        let (joiner, handler) = launch(&local, proc, DriveMode::FireAndForget);

        local
            .run_until(async {
                assert!(handler.try_nudge().is_ok());

                let out = joiner.await.unwrap().unwrap();
                task.output = Some(Output::from(out));
            })
            .await;

        assert!(handler.is_done());
        assert_eq!(handler.state(), ShellState::Finished);

        assert!(task.output.clone().unwrap().clone().status.success());

        let output = task.output.clone().unwrap().clone().stdout;
        let output = String::from_utf8_lossy(&output);
        assert_eq!(output.strip_suffix('\n').unwrap(), "thanks rust!");
    }

    #[tokio::test]
    async fn test_run_cmd_failed() {
        // test run `wrong_echo_unavail_cmd "thanks rust!"` the command spawn failed immediatly.
        let mut task = ShellTask::new("wrong_echo_unavail_cmd", ["thanks rust!"], None);
        let proc = task.proc.take().unwrap();
        let local = tokio::task::LocalSet::new();
        let (joiner, handler) = launch(&local, proc, DriveMode::FireAndForget);

        local
            .run_until(async {
                assert!(handler.try_nudge().is_ok());

                let out = joiner.await.unwrap();
                task.output = out.map(Output::from);
            })
            .await;

        assert!(matches!(handler.state(), ShellState::Failed(..)));
        assert!(task.output.is_none());

        // test run `cat -xx` the command spawned but lead to an error.
        let mut task = ShellTask::new("cat", ["-xx"], None);
        let proc = task.proc.take().unwrap();
        let local = tokio::task::LocalSet::new();
        let (joiner, handler) = launch(&local, proc, DriveMode::FireAndForget);

        local
            .run_until(async {
                assert!(handler.try_nudge().is_ok());

                let out = joiner.await.unwrap();
                task.output = out.map(Output::from);
            })
            .await;

        assert!(matches!(handler.state(), ShellState::Failed(..)));
        assert_eq!(task.output.clone().unwrap().clone().status.code(), Some(1));
    }

    #[tokio::test]
    async fn test_sleep_async() {
        // test run `sleep 0.1` of 100 processes but quickly finished <= 1s (~0.1s whithout much
        // overhead)
        let local = tokio::task::LocalSet::new();

        let start_time = Instant::now();
        local
            .run_until(async {
                let tasks: Vec<_> = (0..100)
                    .map(|_| ShellTask::new("sleep", ["0.1"], None))
                    .collect();
                let mut controllers = Vec::new();
                for mut task in tasks {
                    let proc = task.proc.take().unwrap();
                    let (joiner, handler) = launch(&local, proc, DriveMode::FireAndForget);
                    assert!(handler.try_nudge().is_ok());
                    controllers.push((joiner, handler));
                }

                for (joiner, _) in controllers {
                    let _ = joiner.await;
                }
            })
            .await;
        assert!(start_time.elapsed().as_secs_f64() < 1.0);
    }

    #[tokio::test]
    async fn test_sleep_sync() {
        // test run `sleep 0.1` of 5 processes but slowly finished ~ 0.5s
        let local = tokio::task::LocalSet::new();

        let start_time = Instant::now();
        local
            .run_until(async {
                let tasks: Vec<_> = (0..5)
                    .map(|_| ShellTask::new("sleep", ["0.1"], None))
                    .collect();
                let mut controllers = Vec::new();
                for mut task in tasks {
                    let proc = task.proc.take().unwrap();
                    let (joiner, handler) = launch(&local, proc, DriveMode::FireAndForget);
                    assert!(handler.try_nudge().is_ok());
                    let joiner = joiner.await;
                    controllers.push((joiner, handler));
                }
            })
            .await;
        assert!(start_time.elapsed().as_secs_f64() > 0.4);
    }

    #[tokio::test]
    async fn test_pause_resume() {
        let mut task = ShellTask::new("sleep", ["0.1"], None);
        let proc = task.proc.take().unwrap();
        let local = tokio::task::LocalSet::new();
        let (joiner, mut handler) = launch(&local, proc, DriveMode::Step);

        local
            .run_until(async {
                assert!(handler.try_nudge().is_ok());
                let new_state = handler.wait_for_state_change().await;
                assert_eq!(new_state.as_ref(), Some(&ShellState::Running));

                assert!(handler.try_nudge().is_ok());
                let new_state = handler.wait_for_state_change().await;
                assert_eq!(new_state.as_ref(), Some(&ShellState::Waiting));

                assert!(handler.pause().await.is_ok());
                assert!(handler.try_nudge().is_ok());
                let new_state = handler.wait_for_state_change().await;
                assert_eq!(new_state.as_ref(), Some(&ShellState::Paused));

                assert!(handler.try_nudge().is_ok());
                assert!(handler.try_nudge().is_err());
                assert!(handler.try_nudge().is_err());
                assert!(handler.try_nudge().is_err());

                // TODO: the process should able to mount the state change hook to send in and
                // bring more information in and out.
                // This might able to be tested by inspect tracing?
                //
                // check proc is stopped through watching pid
                // let pid = proc.child.as_ref().unwrap().id().unwrap();
                // let wait_state = waitpid(
                //     #[allow(clippy::cast_possible_wrap)]
                //     Pid::from_raw(pid as i32),
                //     // dont use WaitPidFlag::WNOHANG which not block till the stop signal
                //     Some(WaitPidFlag::WUNTRACED),
                // )
                // .unwrap();
                // assert!(matches!(wait_state, WaitStatus::Stopped(..)));

                handler.resume();
                let new_state = handler.wait_for_state_change().await;
                assert_eq!(new_state.as_ref(), Some(&ShellState::Waiting));

                // let wait_state = waitpid(
                //     #[allow(clippy::cast_possible_wrap)]
                //     Pid::from_raw(pid as i32),
                //     Some(WaitPidFlag::WNOHANG | WaitPidFlag::WUNTRACED),
                // )
                // .unwrap();
                // assert!(matches!(wait_state, WaitStatus::StillAlive));

                while !handler.is_done() {
                    handler.nudge().await;
                }

                let out = joiner.await.unwrap().unwrap();
                task.output = Some(Output::from(out));
            })
            .await;

        assert_eq!(handler.state(), ShellState::Finished);
    }

    #[tokio::test]
    async fn test_kill() {
        let mut task = ShellTask::new("sleep", ["5"], None);
        let proc = task.proc.take().unwrap();
        let local = tokio::task::LocalSet::new();
        let (joiner, mut handler) = launch(&local, proc, DriveMode::Step);

        local
            .run_until(async {
                assert!(handler.try_nudge().is_ok());
                let new_state = handler.wait_for_state_change().await;
                assert_eq!(new_state.as_ref(), Some(&ShellState::Running));

                assert!(handler.try_nudge().is_ok());
                let new_state = handler.wait_for_state_change().await;
                assert_eq!(new_state.as_ref(), Some(&ShellState::Waiting));

                assert!(handler.kill().await.is_ok());
                assert!(handler.try_nudge().is_ok());

                while !handler.is_done() {
                    handler.nudge().await;
                }

                let out = joiner.await.unwrap();
                task.output = out.map(Output::from);
            })
            .await;

        // Unix specific using `signal()`, using `code()` will return None.
        // https://doc.rust-lang.org/nightly/std/process/struct.ExitStatus.html#method.code
        // SIGKILL (9)
        let exit_code = task.output.unwrap().clone().status.signal().unwrap();
        assert_eq!(handler.state(), ShellState::Killed);
        assert_eq!(exit_code, 9);
    }

    #[tokio::test]
    async fn test_pause_kill() {
        let mut task = ShellTask::new("sleep", ["0.1"], None);
        let proc = task.proc.take().unwrap();
        let local = tokio::task::LocalSet::new();
        let (joiner, mut handler) = launch(&local, proc, DriveMode::Step);

        local
            .run_until(async {
                assert!(handler.try_nudge().is_ok());
                let new_state = handler.wait_for_state_change().await;
                assert_eq!(new_state.as_ref(), Some(&ShellState::Running));

                assert!(handler.try_nudge().is_ok());
                let new_state = handler.wait_for_state_change().await;
                assert_eq!(new_state.as_ref(), Some(&ShellState::Waiting));

                assert!(handler.pause().await.is_ok());
                assert!(handler.try_nudge().is_ok());
                let new_state = handler.wait_for_state_change().await;
                assert_eq!(new_state.as_ref(), Some(&ShellState::Paused));

                assert!(handler.try_nudge().is_ok());
                assert!(handler.try_nudge().is_err());
                assert!(handler.try_nudge().is_err());
                assert!(handler.try_nudge().is_err());

                // racing between pause and kill operations, so in this state we dont know
                // what is the exact state of os process, can be either SIGKILL or SIGSTOP

                assert!(handler.kill().await.is_ok());

                let out = joiner.await.unwrap();
                task.output = out.map(Output::from);
            })
            .await;

        assert_eq!(handler.state(), ShellState::Killed);
    }

    #[tokio::test]
    async fn test_pipe_stdin() {
        // test to cover `echo -n "apple\norange\n" | sort` the output of echo pass to sort as the
        // stdin.
        let mut task = ShellTask::new(
            "sort",
            [],
            Some("apple\nbanana\napple\norange\nbanana\napple"),
        );
        let proc = task.proc.take().unwrap();
        let local = tokio::task::LocalSet::new();
        let (joiner, handler) = launch(&local, proc, DriveMode::FireAndForget);

        local
            .run_until(async {
                assert!(handler.try_nudge().is_ok());

                let out = joiner.await.unwrap();
                task.output = out.map(Output::from);
            })
            .await;

        assert!(matches!(handler.state(), ShellState::Finished));
        let output = task.output.clone().unwrap().clone().stdout;
        let output = String::from_utf8_lossy(&output);
        assert_eq!(
            output.strip_suffix('\n').unwrap(),
            "apple\napple\napple\nbanana\nbanana\norange"
        );
    }
}
