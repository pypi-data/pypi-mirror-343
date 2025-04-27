// The buildin arithmetic operations are implemented as tasks which are not necessary.
// Simply here as placeholder for consistency.
// If found in the future there are no complicity such as state transition tracing required to be
// added, implement using rust call instead of building a task.
use tracing::instrument;

use crate::lang::ast::{Op, Operator};
use crate::runtime::core::{Process, State as StateTrait};

#[derive(PartialEq, Clone, Debug)]
pub enum State {
    Begin,
    End,
}

#[derive(Debug)]
enum Event {
    Finish,
    Pause,
    Terminate,
}

impl StateTrait for State {
    fn init() -> Self {
        State::Begin
    }
    fn is_done(&self) -> bool {
        self == &State::End
    }

    // never paused
    fn is_paused(&self) -> bool {
        false
    }
}

impl State {
    fn next(&self, event: Event) -> State {
        match (self, event) {
            (State::Begin, Event::Finish | Event::Terminate) => State::End,
            (s, e) => {
                panic!("Wrong state, event combination: state - {s:#?}, event - {e:#?}")
            }
        }
    }
}

#[derive(Debug, Clone)]
pub enum BaseTyp {
    Number(f64),
    Bool(bool),
    Str(String),
}

const ERROR_MARGIN: f64 = 1e-6;

impl std::fmt::Display for BaseTyp {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            BaseTyp::Number(n) => write!(f, "{n}"),
            BaseTyp::Bool(b) => write!(f, "{b}"),
            BaseTyp::Str(s) => write!(f, "{s}"),
        }
    }
}

impl From<f64> for BaseTyp {
    fn from(value: f64) -> Self {
        BaseTyp::Number(value)
    }
}

impl From<bool> for BaseTyp {
    fn from(value: bool) -> Self {
        BaseTyp::Bool(value)
    }
}

impl From<String> for BaseTyp {
    fn from(value: String) -> Self {
        BaseTyp::Str(value)
    }
}

impl From<&str> for BaseTyp {
    fn from(value: &str) -> Self {
        BaseTyp::Str(value.to_string())
    }
}

#[derive(Debug)]
pub struct BinaryProc {
    state: State,
    operator: Operator,
    inp1: BaseTyp,
    inp2: BaseTyp,
    output: Option<BaseTyp>,
}

impl BinaryProc {
    fn execute(&mut self) {
        self.output = match self.operator.op {
            Op::Plus => match (&self.inp1, &self.inp2) {
                (BaseTyp::Number(inp1), BaseTyp::Number(inp2)) => {
                    Some(BaseTyp::Number(inp1 + inp2))
                }
                (BaseTyp::Str(inp1), BaseTyp::Str(inp2)) => {
                    let str_conc = inp1.to_string() + inp2;
                    Some(BaseTyp::Str(str_conc))
                }
                _ => {
                    unreachable!()
                }
            },
            Op::Minus => match (&self.inp1, &self.inp2) {
                (BaseTyp::Number(inp1), BaseTyp::Number(inp2)) => {
                    Some(BaseTyp::Number(inp1 - inp2))
                }
                _ => {
                    unreachable!()
                }
            },
            Op::Mul => match (&self.inp1, &self.inp2) {
                (BaseTyp::Number(inp1), BaseTyp::Number(inp2)) => {
                    Some(BaseTyp::Number(inp1 * inp2))
                }
                _ => {
                    unreachable!()
                }
            },
            Op::Div => match (&self.inp1, &self.inp2) {
                (BaseTyp::Number(inp1), BaseTyp::Number(inp2)) => {
                    Some(BaseTyp::Number(inp1 / inp2))
                }
                _ => {
                    unreachable!()
                }
            },
            Op::Pow => match (&self.inp1, &self.inp2) {
                (BaseTyp::Number(inp1), BaseTyp::Number(inp2)) => {
                    Some(BaseTyp::Number(inp1.powf(*inp2)))
                }
                _ => {
                    unreachable!()
                }
            },
            Op::Log => match (&self.inp1, &self.inp2) {
                (BaseTyp::Number(inp1), BaseTyp::Number(inp2)) => {
                    Some(BaseTyp::Number(inp1.log(*inp2)))
                }
                _ => {
                    unreachable!()
                }
            },
            Op::EqualEqual => {
                let ret = eq(&self.inp1, &self.inp2);
                Some(BaseTyp::Bool(ret))
            }
            Op::NotEqual => {
                let ret = eq(&self.inp1, &self.inp2);
                Some(BaseTyp::Bool(!ret))
            }
            Op::Less => match (&self.inp1, &self.inp2) {
                (BaseTyp::Number(inp1), BaseTyp::Number(inp2)) => Some(BaseTyp::Bool(inp1 < inp2)),
                _ => {
                    unreachable!()
                }
            },
            Op::LessEqual => match (&self.inp1, &self.inp2) {
                (BaseTyp::Number(inp1), BaseTyp::Number(inp2)) => Some(BaseTyp::Bool(inp1 <= inp2)),
                _ => {
                    unreachable!()
                }
            },
            Op::Greater => match (&self.inp1, &self.inp2) {
                (BaseTyp::Number(inp1), BaseTyp::Number(inp2)) => Some(BaseTyp::Bool(inp1 > inp2)),
                _ => {
                    unreachable!()
                }
            },
            Op::GreaterEqual => match (&self.inp1, &self.inp2) {
                (BaseTyp::Number(inp1), BaseTyp::Number(inp2)) => Some(BaseTyp::Bool(inp1 >= inp2)),
                _ => {
                    unreachable!()
                }
            },
            Op::Or => unreachable!(),
            Op::And => unreachable!(),
            Op::Bang => unreachable!(),
            Op::EigenBool => unreachable!(),
            Op::Equal => unreachable!(),
        }
    }
}

fn eq(inp1: &BaseTyp, inp2: &BaseTyp) -> bool {
    match (inp1, inp2) {
        (BaseTyp::Bool(inp1), BaseTyp::Bool(inp2)) => inp1 == inp2,
        (BaseTyp::Str(inp1), BaseTyp::Str(inp2)) => inp1 == inp2,
        (BaseTyp::Number(inp1), BaseTyp::Number(inp2)) => (inp1 - inp2).abs() < ERROR_MARGIN,
        _ => false,
    }
}

impl Process<State> for BinaryProc {
    type Output = BaseTyp;

    fn state(&self) -> &State {
        &self.state
    }
    fn transition_to(&mut self, state: State) {
        self.state = state;
    }
    fn is_done(&self) -> bool {
        self.state().is_done()
    }
    fn is_paused(&self) -> bool {
        self.state().is_paused()
    }
    fn output(&self) -> Option<Self::Output> {
        self.output.clone()
    }
    async fn kill(&mut self) -> State {
        self.state = self.state.next(Event::Terminate);
        self.state.clone()
    }
    async fn pause(&mut self) -> State {
        self.state = self.state.next(Event::Pause);
        self.state.clone()
    }

    #[instrument(name = "bin_proc_advance", skip(self))]
    async fn advance(&mut self) -> State {
        self.state = match self.state {
            State::Begin => {
                self.execute();
                tracing::trace!(
                    "compute binary expression: {} {} {} = {}",
                    self.inp1,
                    self.operator,
                    self.inp2,
                    self.output.clone().expect("output not avail")
                );

                self.state.next(Event::Finish)
            }
            State::End => unreachable!(),
        };
        self.state.clone()
    }
}

impl BinaryProc {
    fn new(operator: &Operator, inp1: &BaseTyp, inp2: &BaseTyp) -> Self {
        BinaryProc {
            state: State::Begin,
            operator: operator.clone(),
            inp1: inp1.clone(),
            inp2: inp2.clone(),
            output: None,
        }
    }
}

pub struct BinaryTask {
    // input: (BaseTyp, BaseTyp),
    pub output: Option<BaseTyp>,
    pub proc: Option<BinaryProc>,
}

impl BinaryTask {
    #[must_use]
    pub fn new(op: &Operator, inp1: &BaseTyp, inp2: &BaseTyp) -> Self {
        let input = (inp1, inp2);
        let proc = Some(BinaryProc::new(op, input.0, input.1));
        BinaryTask {
            // input: (inp1.clone(), inp2.clone()),
            output: None,
            proc,
        }
    }
}
