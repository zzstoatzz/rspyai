use std::fs;
use std::io;
use std::path::Path;
use syn::{parse_file, Item};
use walkdir::WalkDir;

use crate::debug::debug_log;
use crate::function::RustFunction;

pub struct ProjectScanner;

impl ProjectScanner {
    pub fn scan_directory(dir_path: &Path) -> io::Result<Vec<RustFunction>> {
        let mut functions = Vec::new();

        if dir_path.is_dir() {
            for entry in WalkDir::new(dir_path)
                .follow_links(true)
                .into_iter()
                .filter_map(|e| e.ok())
            {
                let path = entry.path();
                if path.extension().map_or(false, |ext| ext == "rs") {
                    if let Some(file_functions) = Self::scan_file(path) {
                        functions.extend(file_functions);
                    }
                }
            }
        }
        Ok(functions)
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
