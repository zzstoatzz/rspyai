use pyo3::prelude::*;

/// Get metadata about a Rust function
#[pyfunction]
fn get_function_metadata(name: &str) -> PyResult<String> {
    // For now, just return basic info about the function
    Ok(format!("Function: {}\nType: Rust\nStatus: Available", name))
}

/// A simple test function that we'll use as an example
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn rspyai(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(get_function_metadata, m)?)?;
    Ok(())
}
