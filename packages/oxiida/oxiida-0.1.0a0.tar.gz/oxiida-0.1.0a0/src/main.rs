use std::collections::HashSet;
use std::fs;
use std::path::PathBuf;

use clap::{Parser, Subcommand};
use miette::IntoDiagnostic;
use oxiida::runtime::ffi::{FFIHandler, NullActor};
use tracing::Level;

use oxiida::lang::lex::{LalrLexer, Lexer, LexicalError};
use oxiida::lang::parser::parse_stmt;
use oxiida::runtime::{self, FilePersistence, NullPersistence, PersistenceHandler, VarEnv};

#[derive(Parser)]
#[command(version, about, long_about = None)]
struct Args {
    /// Turn debugging information on
    #[arg(short, long, action = clap::ArgAction::Count)]
    debug: u8,

    #[command(subcommand)]
    command: Option<Commands>,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// lexing
    Lex {
        /// source file to lexing
        source_file: PathBuf,
    },

    /// parse
    Parse { source_file: PathBuf },

    /// evaluate
    Evaluate { source_file: PathBuf },

    /// run
    Run {
        source_file: PathBuf,

        #[arg(short, long)]
        storage: Option<String>,
    },

    /// does testing things
    Test {
        /// lists test values
        #[arg(short, long)]
        list: bool,
    },
}

#[allow(clippy::too_many_lines)]
#[tokio::main()]
async fn main() -> miette::Result<()> {
    let subscriber = tracing_subscriber::fmt()
        .compact()
        .with_file(true)
        .with_line_number(true)
        .with_thread_ids(true)
        .with_target(false)
        .with_max_level(Level::DEBUG)
        .finish();
    tracing::subscriber::set_global_default(subscriber).into_diagnostic()?;

    let args = Args::parse();
    let command = args.command;

    match command {
        Some(Commands::Lex { source_file }) => {
            let file_contents = fs::read_to_string(&source_file).unwrap_or_else(|_| {
                eprintln!("Failed to read file {}", source_file.to_string_lossy());
                String::new()
            });

            let mut any_cc_err = false;
            for token in Lexer::new(file_contents.as_str()) {
                match token {
                    Err(LexicalError::SingleTokenError(unrecognized)) => {
                        any_cc_err = true;
                        eprintln!(
                            "[line {}] Error: Unexpected character: {}",
                            unrecognized.line(),
                            unrecognized.token,
                        );
                        eprintln!("{:?}", miette::Report::new(unrecognized));
                    }
                    Err(LexicalError::StringUnterminatedError(unrecognized)) => {
                        any_cc_err = true;
                        eprintln!("[line {}] Error: Unterminated string.", unrecognized.line(),);
                        eprintln!("{:?}", miette::Report::new(unrecognized));
                    }
                    Err(LexicalError::NumberParseError(unrecognized)) => {
                        any_cc_err = true;
                        eprintln!(
                            "[line {}] Error: Unable to parse number.",
                            unrecognized.line(),
                        );
                        eprintln!("{:?}", miette::Report::new(unrecognized));
                    }
                    Ok(token) => {
                        println!("{token}");
                    }
                }
            }
            println!("EOF  null");

            if any_cc_err {
                std::process::exit(65)
            };
        }
        Some(Commands::Parse { source_file }) => {
            let file_contents = fs::read_to_string(&source_file).unwrap_or_else(|_| {
                eprintln!("Failed to read file {}", source_file.to_string_lossy());
                String::new()
            });

            let lexer = LalrLexer::new(file_contents.as_str());
            let stmts = parse_stmt(lexer, file_contents.as_str()).unwrap_or_else(|e| {
                eprintln!("{e:?}");
                std::process::exit(65)
            });
            for stmt in stmts {
                println!("{stmt}");
            }
        }
        Some(Commands::Run {
            source_file,
            storage,
        }) => {
            let file_contents = fs::read_to_string(&source_file).unwrap_or_else(|_| {
                eprintln!("Failed to read file {}", source_file.to_string_lossy());
                String::new()
            });

            let lexer = LalrLexer::new(file_contents.as_str());
            let stmts = parse_stmt(lexer, file_contents.as_str())?;

            let local = tokio::task::LocalSet::new();
            let mut glb_var_env = VarEnv::new(HashSet::new());

            let persistence_handler = if let Some(storage) = storage {
                match storage.to_uppercase().as_str() {
                    "FILE" => PersistenceHandler::new(FilePersistence::new),
                    _ => panic!("unknown storage type {storage}"),
                }
            } else {
                PersistenceHandler::new(NullPersistence::new)
            };
            let ffi_handler = FFIHandler::new("nil", NullActor::new);

            local
                .run_until(async {
                    let wf = runtime::interpret(
                        stmts,
                        &mut glb_var_env,
                        persistence_handler.clone(),
                        ffi_handler.clone(),
                        &file_contents,
                    );
                    wf.await?;
                    Ok::<_, miette::Error>(())
                })
                .await?;
        }
        _ => {
            todo!()
        }
    }

    Ok(())
}
