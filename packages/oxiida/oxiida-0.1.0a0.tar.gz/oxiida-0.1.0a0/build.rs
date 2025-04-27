use std::env::current_dir;

fn main() {
    lalrpop::Configuration::new()
        .set_in_dir(current_dir().unwrap().join("src/lang"))
        .process()
        .unwrap();
}
