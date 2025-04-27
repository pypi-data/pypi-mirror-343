use miette::{Diagnostic, Result, SourceSpan};
use thiserror::Error;

#[derive(Error, Diagnostic, Debug, Clone)]
pub enum LexicalError {
    #[error(transparent)]
    #[diagnostic(transparent)]
    SingleTokenError(#[from] SingleTokenError),

    #[error(transparent)]
    #[diagnostic(transparent)]
    StringUnterminatedError(#[from] StringUnterminatedError),

    #[error(transparent)]
    #[diagnostic(transparent)]
    NumberParseError(#[from] NumberParseError),
}

#[derive(Diagnostic, Debug, Error, Clone)]
#[error("Unexpected token '{token}' in input")]
pub struct SingleTokenError {
    #[source_code]
    src: String,

    pub token: char,

    #[label = "this input character"]
    err_span: SourceSpan,
}

impl SingleTokenError {
    #[must_use]
    pub fn line(&self) -> usize {
        let until_unrecogonized = &self.src[..=self.err_span.offset()];
        until_unrecogonized.lines().count()
    }
}

#[derive(Diagnostic, Debug, Error, Clone)]
#[error("Unterminated string")]
pub struct StringUnterminatedError {
    #[source_code]
    src: String,

    #[label = "this string"]
    err_span: SourceSpan,
}

impl StringUnterminatedError {
    #[must_use]
    pub fn line(&self) -> usize {
        let until_unrecogonized = &self.src[..self.err_span.offset()];
        until_unrecogonized.lines().count()
    }
}

#[derive(Diagnostic, Debug, Error, Clone)]
#[error("Unable to parse number")]
pub struct NumberParseError {
    #[source_code]
    src: String,

    #[label = "this number"]
    err_span: SourceSpan,
}

impl NumberParseError {
    #[must_use]
    pub fn line(&self) -> usize {
        let until_unrecogonized = &self.src[..self.err_span.offset()];
        until_unrecogonized.lines().count()
    }
}

#[derive(Debug, PartialEq, Clone)]
pub struct Token<'input> {
    whole: &'input str,
    kind: TokenKind,
    bloc: usize,
    eloc: usize,
}

#[derive(Debug, PartialEq, Clone)]
pub enum TokenKind {
    LeftParen,
    RightParen,
    LeftBrace,
    RightBrace,
    LeftBraket,
    RightBraket,
    Comma,
    Dot,
    Minus,
    Plus,
    Caret,
    Semicolon,
    Star,
    Equal,
    EqualEqual,
    Bang,
    BangEqual,
    Less,
    LessEqual,
    Greater,
    GreaterEqual,
    Slash,
    Pipe,
    String(String),
    Literal(String),
    Number(f64),
    Identifier(String),
    Shell,
    ShellPipe,
    And,
    In,
    Class,
    Else,
    False,
    For,
    Def,
    Seq,
    Para,
    If,
    Nil,
    Or,
    Return,
    Super,
    This,
    True,
    Var,
    While,
    Print,
    Require,
    // Error is specified for Lalrpop
    Error,
}

impl std::fmt::Display for Token<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        // dbg!(self);
        let i = &self.whole[self.bloc..=self.eloc];
        match self.kind {
            TokenKind::LeftParen => write!(f, "LEFT_PAREN {i} null"),
            TokenKind::RightParen => write!(f, "RIGHT_PAREN {i} null"),
            TokenKind::LeftBrace => write!(f, "LEFT_BRACE {i} null"),
            TokenKind::RightBrace => write!(f, "RIGHT_BRACE {i} null"),
            TokenKind::LeftBraket => write!(f, "LEFT_BRAKET {i} null"),
            TokenKind::RightBraket => write!(f, "RIGHT_BRAKET {i} null"),
            TokenKind::Comma => write!(f, "COMMA {i} null"),
            TokenKind::Dot => write!(f, "DOT {i} null"),
            TokenKind::Minus => write!(f, "MINUS {i} null"),
            TokenKind::Plus => write!(f, "PLUS {i} null"),
            TokenKind::Caret => write!(f, "CARET {i} null"),
            TokenKind::Semicolon => write!(f, "SEMICOLON {i} null"),
            TokenKind::Star => write!(f, "STAR {i} null"),
            TokenKind::Equal => write!(f, "EQUAL {i} null"),
            TokenKind::EqualEqual => write!(f, "EQUAL_EQUAL {i} null"),
            TokenKind::Bang => write!(f, "BANG {i} null"),
            TokenKind::BangEqual => write!(f, "BANG_EQUAL {i} null"),
            TokenKind::Less => write!(f, "LESS {i} null"),
            TokenKind::LessEqual => write!(f, "LESS_EQUAL {i} null"),
            TokenKind::Greater => write!(f, "GREATER {i} null"),
            TokenKind::GreaterEqual => write!(f, "GREATER_EQUAL {i} null"),
            TokenKind::Slash => write!(f, "SLASH {i} null"),
            TokenKind::Pipe => write!(f, "PIPE {i} null"),
            TokenKind::String(_) => write!(f, "STRING \"{i}\" {i}"),
            TokenKind::Number(n) => write!(f, "NUMBER {i} {n}"),
            TokenKind::Literal(_) => write!(f, "LITERAL {i} null"),
            TokenKind::Identifier(_) => write!(f, "IDENTIFIER {i} null"),
            TokenKind::Shell => write!(f, "SHELL {i} null"),
            TokenKind::ShellPipe => write!(f, "SHELL_PIPE {i} null"),
            TokenKind::And => write!(f, "AND {i} null"),
            TokenKind::In => write!(f, "IN {i} null"),
            TokenKind::Class => write!(f, "CLASS {i} null"),
            TokenKind::Else => write!(f, "ELSE {i} null"),
            TokenKind::False => write!(f, "FALSE {i} null"),
            TokenKind::For => write!(f, "FOR {i} null"),
            TokenKind::Def => write!(f, "DEF {i} null"),
            TokenKind::Seq => write!(f, "SEQ {i} null"),
            TokenKind::Para => write!(f, "PARA {i} null"),
            TokenKind::If => write!(f, "IF {i} null"),
            TokenKind::Nil => write!(f, "NIL {i} null"),
            TokenKind::Or => write!(f, "OR {i} null"),
            TokenKind::Return => write!(f, "RETURN {i} null"),
            TokenKind::Super => write!(f, "SUPER {i} null"),
            TokenKind::This => write!(f, "THIS {i} null"),
            TokenKind::True => write!(f, "TRUE {i} null"),
            TokenKind::Var => write!(f, "VAR {i} null"),
            TokenKind::While => write!(f, "WHILE {i} null"),
            TokenKind::Print => write!(f, "PRINT {i} null"),
            TokenKind::Require => write!(f, "REQUIRE {i} null"),
            TokenKind::Error => write!(f, "Error {i} null"),
        }
    }
}

// TODO: rename to SpanIter
#[derive(Debug)]
pub struct Lexer<'input> {
    rest: &'input str,
    whole: &'input str,
    byte: usize,
}

impl<'input> Lexer<'input> {
    #[must_use]
    pub fn new(input: &'input str) -> Self {
        Lexer {
            rest: input,
            whole: input,
            byte: 0,
        }
    }
}

impl<'input> Iterator for Lexer<'input> {
    type Item = Result<Token<'input>, LexicalError>;

    #[allow(clippy::too_many_lines)]
    fn next(&mut self) -> Option<Self::Item> {
        enum Started {
            IfEqualElse(TokenKind, TokenKind),
            Literal,
            Number,
            Slash,
            String,
        }

        loop {
            // dbg!(self.rest);
            let mut chars = self.rest.chars();
            let c = chars.next()?;
            let c_onwards = self.rest;
            self.rest = chars.as_str();
            let bloc = self.byte;
            self.byte += c.len_utf8();

            let just = |kind: TokenKind,
                        bloc: usize,
                        eloc: usize|
             -> Option<std::result::Result<Token<'_>, LexicalError>> {
                Some(Ok(Token {
                    whole: self.whole,
                    kind,
                    bloc,
                    eloc,
                }))
            };

            let started = match c {
                '(' => return just(TokenKind::LeftParen, bloc, self.byte - 1),
                ')' => return just(TokenKind::RightParen, bloc, self.byte - 1),
                '{' => return just(TokenKind::LeftBrace, bloc, self.byte - 1),
                '}' => return just(TokenKind::RightBrace, bloc, self.byte - 1),
                '[' => return just(TokenKind::LeftBraket, bloc, self.byte - 1),
                ']' => return just(TokenKind::RightBraket, bloc, self.byte - 1),
                ',' => return just(TokenKind::Comma, bloc, self.byte - 1),
                '.' => return just(TokenKind::Dot, bloc, self.byte - 1),
                '-' => return just(TokenKind::Minus, bloc, self.byte - 1),
                '+' => return just(TokenKind::Plus, bloc, self.byte - 1),
                '^' => return just(TokenKind::Caret, bloc, self.byte - 1),
                ';' => return just(TokenKind::Semicolon, bloc, self.byte - 1),
                '*' => return just(TokenKind::Star, bloc, self.byte - 1),
                '|' => return just(TokenKind::Pipe, bloc, self.byte - 1),
                '=' => Started::IfEqualElse(TokenKind::EqualEqual, TokenKind::Equal),
                '!' => Started::IfEqualElse(TokenKind::BangEqual, TokenKind::Bang),
                '>' => Started::IfEqualElse(TokenKind::GreaterEqual, TokenKind::Greater),
                '<' => Started::IfEqualElse(TokenKind::LessEqual, TokenKind::Less),
                '/' => Started::Slash,
                '0'..='9' => Started::Number,
                'a'..='z' | 'A'..='Z' | '_' => Started::Literal,
                '"' => Started::String,
                c if c.is_whitespace() => continue,
                _ => {
                    return Some(Err(SingleTokenError {
                        src: self.whole.to_string(),
                        token: c,
                        err_span: SourceSpan::from(self.byte - c.len_utf8()..self.byte),
                    }
                    .into()))
                }
            };

            match started {
                Started::Slash => {
                    if self.rest.starts_with('/') {
                        let line_end = self.rest.find('\n').unwrap_or(self.rest.len());
                        self.byte += line_end;
                        self.rest = &self.rest[line_end..];
                        continue;
                    }
                    return just(TokenKind::Slash, bloc, bloc);
                }
                Started::IfEqualElse(yes, no) => {
                    let eloc = self.byte;
                    self.rest = self.rest.trim_start();
                    let trimmed = c_onwards.len() - self.rest.len() - 1;
                    self.byte += trimmed;
                    if self.rest.starts_with('=') {
                        self.rest = &self.rest[1..];
                        self.byte += 1;
                        return Some(Ok(Token {
                            whole: self.whole,
                            kind: yes,
                            bloc,
                            eloc: bloc + trimmed + 1,
                        }));
                    }
                    return just(no, bloc, eloc - 1);
                }
                Started::Number => {
                    let first_non_digit = c_onwards
                        .find(|c| !matches!(c, '0'..='9' | '_' | '.'))
                        .unwrap_or(c_onwards.len());

                    let literal = &c_onwards[..first_non_digit];
                    // dbg!(literal);
                    let mut dotted = literal.splitn(3, '.');
                    let literal = if let (Some(one), Some(two), _) =
                        (dotted.next(), dotted.next(), dotted.next())
                    {
                        if two.is_empty() {
                            self.byte += one.len();
                            self.rest = &c_onwards[one.len()..];
                            &literal[..one.len()]
                        } else {
                            self.byte += one.len() + two.len();
                            self.rest = &c_onwards[one.len() + 1 + two.len()..];
                            &literal[..one.len() + 1 + two.len()]
                        }
                    } else {
                        self.byte += literal.len() - 1;
                        self.rest = &c_onwards[literal.len()..];
                        literal
                    };
                    let Ok(n) = literal.parse::<f64>() else {
                        return Some(Err(NumberParseError {
                            src: self.whole.to_string(),
                            err_span: SourceSpan::from(self.byte - literal.len()..self.byte),
                        }
                        .into()));
                    };

                    let eloc = bloc + literal.len() - 1;
                    return Some(Ok(Token {
                        whole: self.whole,
                        kind: TokenKind::Number(n),
                        bloc,
                        eloc,
                    }));
                }
                Started::Literal => {
                    let not_literal = self
                        .rest
                        .find(|c| !matches!(c, 'a'..='z' | 'A'..='Z' | '0'..='9' | '_'))
                        .unwrap_or(c_onwards.len() - 1);

                    let literal = &c_onwards[..=not_literal];
                    let eloc = bloc + literal.len() - 1;
                    self.byte += literal.len() - 1;
                    self.rest = &c_onwards[literal.len()..];
                    let token_kind = match literal {
                        "shell" => TokenKind::Shell,
                        "shellpipe" => TokenKind::ShellPipe,
                        "and" => TokenKind::And,
                        "in" => TokenKind::In,
                        "class" => TokenKind::Class,
                        "else" => TokenKind::Else,
                        "false" => TokenKind::False,
                        "for" => TokenKind::For,
                        "seq" => TokenKind::Seq,
                        "para" => TokenKind::Para,
                        "def" => TokenKind::Def,
                        "if" => TokenKind::If,
                        "nil" => TokenKind::Nil,
                        "or" => TokenKind::Or,
                        "return" => TokenKind::Return,
                        "super" => TokenKind::Super,
                        "this" => TokenKind::This,
                        "true" => TokenKind::True,
                        "var" => TokenKind::Var,
                        "while" => TokenKind::While,
                        "print" => TokenKind::Print,
                        "require" => TokenKind::Require,
                        lit => {
                            return Some(Ok(Token {
                                whole: self.whole,
                                kind: TokenKind::Identifier(lit.to_string()),
                                bloc,
                                eloc,
                            }))
                        }
                    };

                    return Some(Ok(Token {
                        whole: self.whole,
                        kind: token_kind,
                        bloc,
                        eloc,
                    }));
                }
                Started::String => {
                    if let Some(strlen) = self.rest.find('"') {
                        self.byte += strlen;
                        self.rest = &self.rest[strlen + 1..];
                        self.byte += 1;
                        let literal = &c_onwards[1..=strlen];
                        return Some(Ok(Token {
                            whole: self.whole,
                            kind: TokenKind::String(literal.to_string()),
                            // strip the inclose ""
                            bloc: bloc + 1,
                            eloc: self.byte - 2,
                        }));
                    }
                    let start_idx = self.byte;
                    self.byte += self.rest.len();
                    self.rest = &self.rest[self.rest.len()..];
                    return Some(Err(StringUnterminatedError {
                        src: self.whole.to_string(),
                        err_span: SourceSpan::from(start_idx..start_idx + c_onwards.len() - 1),
                    }
                    .into()));
                }
            }
        }
    }
}

pub type Spanned<Tok, Loc, Error> = Result<(Loc, Tok, Loc), Error>;

#[derive(Debug)]
pub struct LalrLexer<'input> {
    token_stream: Lexer<'input>,
}

impl<'input> LalrLexer<'input> {
    #[must_use]
    pub fn new(input: &'input str) -> Self {
        LalrLexer {
            token_stream: Lexer::new(input),
        }
    }
}

impl Iterator for LalrLexer<'_> {
    type Item = Spanned<TokenKind, usize, LexicalError>;

    fn next(&mut self) -> Option<Self::Item> {
        self.token_stream.next().map(|token| {
            if let Err(err) = token {
                match err {
                    LexicalError::SingleTokenError(err) => {
                        eprintln!("{:?}", miette::Report::new(err.clone()));
                        let loc = err.err_span.offset();
                        return Ok((loc, TokenKind::Error, loc));
                    }
                    LexicalError::StringUnterminatedError(err) => {
                        eprintln!("{:?}", miette::Report::new(err.clone()));
                        let loc = err.err_span.offset();
                        let eloc = loc + err.err_span.len();
                        return Ok((loc, TokenKind::Error, eloc));
                    }
                    LexicalError::NumberParseError(err) => {
                        eprintln!("{:?}", miette::Report::new(err.clone()));
                        let loc = err.err_span.offset();
                        let eloc = loc + err.err_span.len();
                        return Ok((loc, TokenKind::Error, eloc));
                    }
                }
            }
            let token = token.expect("lexing error");
            let tok = token.kind;
            Ok((token.bloc, tok, token.eloc))
        })
    }
}
