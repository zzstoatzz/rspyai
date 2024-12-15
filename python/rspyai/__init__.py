"""Python bindings for the rspyai Rust library."""

from .rspyai import get_function_metadata, scan_rust_project

__all__ = ['scan_rust_project', 'get_function_metadata']
