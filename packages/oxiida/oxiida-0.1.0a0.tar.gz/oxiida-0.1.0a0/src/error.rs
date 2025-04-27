use crate::runtime::HandlerEvent;

#[derive(Debug)]
pub enum Error {
    // tokio channel is closed cannot send message to it.
    EventChannelClosed(HandlerEvent),
}

impl std::fmt::Display for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Error::EventChannelClosed(event) => {
                write!(f, "cannot send `{event:?}` event to closed channel")
            }
        }
    }
}
