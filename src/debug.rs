use std::env;

/// Checks if the RSPYAI_DEBUG environment variable is set
pub fn should_debug() -> bool {
    env::var("RSPYAI_DEBUG").is_ok()
}

/// A simple debug log function that prints a message if the RSPYAI_DEBUG environment variable is set
pub fn debug_log(msg: &str) {
    if should_debug() {
        println!("{}", msg);
    }
}
