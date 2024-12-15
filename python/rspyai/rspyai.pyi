"""Type stubs for utility functions used by the TUI (implemented in Rust)."""

def scan_rust_project(file_path: str | None = None) -> list[dict[str, str]]:
    """Scan a Rust project directory and return a list of function metadata."""
    ...

def get_function_metadata(path: str, name: str) -> dict[str, str]:
    """Get detailed metadata about a specific function."""
    ...
