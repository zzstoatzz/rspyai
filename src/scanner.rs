use std::fs;
use std::path::Path;
use syn::{parse_file, Item};
use walkdir::WalkDir;

use crate::debug::debug_log;
use crate::function::RustFunction;

pub struct ProjectScanner;

impl ProjectScanner {
    pub fn scan_directory(root_path: &Path) -> Vec<RustFunction> {
        let mut functions = Vec::new();

        for entry in WalkDir::new(root_path)
            .follow_links(true)
            .into_iter()
            .filter_entry(|e| !Self::should_skip(e.path()))
            .flatten()
        {
            let path = entry.path();
            if path.extension().and_then(|s| s.to_str()) == Some("rs") {
                if let Some(mut file_functions) = Self::scan_file(path) {
                    functions.append(&mut file_functions);
                }
            }
        }

        functions
    }

    fn should_skip(path: &Path) -> bool {
        path.components().any(|c| {
            let s = c.as_os_str().to_string_lossy();
            s == "target" || s.starts_with('.')
        })
    }

    pub fn scan_file(path: &Path) -> Option<Vec<RustFunction>> {
        let is_lib = path.file_name().map_or(false, |f| f == "lib.rs");
        debug_log(&format!("Scanning file: {:?}", path));

        let content = fs::read_to_string(path).ok()?;
        let file = parse_file(&content).ok()?;

        let mut functions = Vec::new();

        for item in file.items {
            if let Item::Fn(func) = item {
                if RustFunction::is_public(&func, is_lib) {
                    functions.push(RustFunction::new(&func, path.to_string_lossy().to_string()));
                }
            }
        }

        Some(functions)
    }
}
