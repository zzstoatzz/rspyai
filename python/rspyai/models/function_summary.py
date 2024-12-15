"""Models for function summaries."""

from typing import Annotated, TypedDict

from pydantic import Field


class FunctionSummary(TypedDict):
    """Summary of a Rust function."""

    purpose: Annotated[str, Field(description='A clear, concise description of what the function does')]
    key_features: Annotated[
        list[str],
        Field(description='List of key features or important aspects of the function'),
    ]
    usage_notes: Annotated[str, Field(description='Important notes about using the function correctly')]
