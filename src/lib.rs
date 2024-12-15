use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use std::collections::HashMap;
use std::path::Path;

mod debug;
mod function;
mod scanner;

use scanner::ProjectScanner;

/// Scans a Rust project directory for public functions that could be exposed to Python
#[pyfunction]
#[pyo3(signature = (file_path = None))]
fn scan_rust_project(py: Python<'_>, file_path: Option<&str>) -> PyResult<Py<PyList>> {
    let functions = PyList::empty(py);

    let root_path = match file_path {
        Some(p) => Path::new(p),
        None => Path::new("src"),
    };

    if let Ok(rust_functions) = ProjectScanner::scan_directory(root_path) {
        for func in rust_functions {
            let dict = PyDict::new(py);
            dict.set_item("name", func.name)?;
            dict.set_item("doc", func.doc)?;
            dict.set_item("signature", func.signature)?;
            dict.set_item("path", func.path)?;
            dict.set_item("source", func.source)?;
            functions.append(dict)?;
        }
    }

    Ok(functions.into())
}

/// Get detailed metadata about a specific Rust function
#[pyfunction]
fn get_function_metadata(path: &str, name: &str) -> PyResult<HashMap<String, String>> {
    let mut metadata = HashMap::new();
    metadata.insert("name".to_string(), name.to_string());
    metadata.insert("path".to_string(), path.to_string());

    if let Some(functions) = ProjectScanner::scan_file(Path::new(path)) {
        if let Some(func) = functions.into_iter().find(|f| f.name == name) {
            metadata.insert("signature".to_string(), func.signature);
            metadata.insert("doc".to_string(), func.doc);
            metadata.insert("source".to_string(), func.source);
            metadata.insert("status".to_string(), "Available".to_string());
            return Ok(metadata);
        }
    }

    metadata.insert("status".to_string(), "Not Found".to_string());
    Ok(metadata)
}

///This is the main module for the rspyai library
#[pymodule]
fn rspyai(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(scan_rust_project, m)?)?;
    m.add_function(wrap_pyfunction!(get_function_metadata, m)?)?;
    Ok(())
}
