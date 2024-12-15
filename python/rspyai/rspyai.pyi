"""Type stubs for utility functions used by the TUI (implemented in Rust)."""

from typing import Literal, TypedDict

class RustFunctionMetadata(TypedDict):
    """Matches the RustFunction struct in function.rs."""

    name: str
    path: str
    signature: str
    doc: str

class FunctionMetadataResponse(RustFunctionMetadata):
    """Response from get_function_metadata including status."""

    status: Literal['Available', 'Not Found']

def scan_rust_project(file_path: str | None = None) -> list[RustFunctionMetadata]:
    """Scan a Rust project directory and return a list of function metadata."""
    ...

def get_function_metadata(path: str, name: str) -> FunctionMetadataResponse:
    """Get detailed metadata about a specific function.

    Returns a dict with function metadata and a status field indicating if the
    function was found.
    """
    ...
