use grammar::StatementsParser;
use lalrpop_util::{lalrpop_mod, ParseError};
use miette::{self, LabeledSpan};

use crate::lang::{ast::Stmt, lex::LalrLexer};

use super::lex::{LexicalError, TokenKind};

lalrpop_mod!(pub grammar);

fn convert_parse_error(
    err: ParseError<usize, TokenKind, LexicalError>,
    src: &str,
) -> miette::Report {
    match err {
        lalrpop_util::ParseError::UnrecognizedEof { location, expected } => miette::miette!(
            code = "parser_stmt::UnrecognizedEof",
            help = "provide more tokens",
            labels = vec![LabeledSpan::at_offset(location, "here")],
            "expect {}",
            expected.join(" "),
        )
        .with_source_code(src.to_string()),
        lalrpop_util::ParseError::UnrecognizedToken { token, expected } => {
            let (bloc, _, eloc) = token;

            miette::miette!(
                code = "parser_stmt::UnrecognizedToken",
                help = "try other tokens",
                labels = vec![LabeledSpan::at(bloc..=eloc, "this")],
                "expect {}",
                expected.join(" "),
            )
            .with_source_code(src.to_string())
        }
        lalrpop_util::ParseError::InvalidToken { location } => miette::miette!(
            code = "parser_stmt::InvalidToken",
            help = "provide valid tokens",
            labels = vec![LabeledSpan::at_offset(location, "here")],
            "invalid token",
        )
        .with_source_code(src.to_string()),
        // TODO:
        // lalrpop_util::ParseError::ExtraToken { token } => todo!(),
        // lalrpop_util::ParseError::User { error } => todo!(),
        _ => todo!(),
    }
}

pub fn parse_stmt(lexer: LalrLexer, src: &str) -> miette::Result<Vec<Stmt>> {
    let mut errors = Vec::new();
    let parser = StatementsParser::new();
    let ast = parser
        .parse(&mut errors, lexer)
        .map_err(|err| convert_parse_error(err, src))?;

    if errors.is_empty() {
        Ok(ast)
    } else {
        for err in errors {
            eprintln!("{:?}", convert_parse_error(err.error, src));
        }
        std::process::exit(65)
    }
}
