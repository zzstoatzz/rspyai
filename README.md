# `rspyai`

A [Textual](https://github.com/textualize/textual/) app to explore your Rust codebase.


## requirements

- [uv](https://docs.astral.sh/uv/) to bootstrap a python environment
- an [`OPENAI_API_KEY`](https://platform.openai.com/docs/api-reference/authentication) set in your environment

## usage

> [!NOTE]
> This project is a personal project. It might break for some reason.

```bash
# start the function browser
uvx rspyai@latest

# start the function scanner at a specific path
uvx rspyai@latest [path_to_rust_project]
```

### interactive TUI

the TUI provides:
- function tree browser
- information on each function: signature, docstring, parent file, etc.
- ai-generated summaries with AI agent summary (`pydantic-ai`)

https://github.com/user-attachments/assets/7fd118c1-3587-4ddc-8aec-a18d88e38f04

## development

```bash
# Clone the repository
git clone https://github.com/zzstoatzz/rspyai.git
cd rspyai

# Install development dependencies
uv sync --dev --all-extras
```