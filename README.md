# rspyai

A [Textual](https://github.com/textualize/textual/) app to explore your Rust codebase.

## Usage

> [!NOTE]
> This project is a personal project. It is easiest run with `uvx`.

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
- AI-generated summaries with Marvin's commentary

## Development

```bash
# Clone the repository
git clone https://github.com/zzstoatzz/rspyai.git
cd rspyai

# Install development dependencies
uv sync --dev --all-extras

# Run tests
uv run pytest

# Run benchmarks
uv run pytest test/test_speed.py -v
```