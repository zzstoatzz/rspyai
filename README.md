# rspyai

A [Textual](https://github.com/textualize/textual/) app to explore your Rust codebase.


## requirements

- [uv](https://docs.astral.sh/uv/)
- [`OPENAI_API_KEY`](https://platform.openai.com/docs/api-reference/authentication)

## usage

> [!NOTE]
> This project is a personal project. It might break for some reason.

```bash
# start the function browser
uvx rspyai

# start the function scanner at a specific path
uvx rspyai [path_to_rust_project]
```

### Interactive TUI

The TUI provides:
- Function tree browser
- Detailed function information
- AI-generated summaries with AI agent summary (`pydantic-ai`)

<p align="center">
  <img src="./assets/rspyai.gif" alt="rspyai" />
</p>

## Development

```bash
# Clone the repository
git clone https://github.com/zzstoatzz/rspyai.git
cd rspyai

# Install development dependencies
uv sync --dev --all-extras
```