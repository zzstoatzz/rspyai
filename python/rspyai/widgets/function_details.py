"""Widget for displaying function details."""

from rich.console import Console, ConsoleOptions, RenderResult
from rich.markdown import CodeBlock, Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static

from rspyai import get_function_metadata
from rspyai.widgets.function_summary import FunctionSummaryWidget


class FullWidthCodeBlock(CodeBlock):
    """Code block that extends background to full width."""

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        """Render the code block."""
        code = str(self.text).rstrip()
        syntax = Syntax(
            code,
            self.lexer_name,
            theme='monokai',
            word_wrap=True,
        )
        yield Panel(
            syntax,
            expand=True,
            style='on rgb(22,22,22)',
            border_style='none',
        )


# Use our custom code block renderer
Markdown.elements['fence'] = FullWidthCodeBlock


class FunctionDetails(Widget):
    """Widget for displaying function details."""

    def compose(self):
        """Create child widgets."""
        with Vertical():  # Main container
            with Vertical(id='function-details'):  # Top half - scrollable details
                yield Static('select a function to view details')
            with Vertical(id='summary-scroll'):  # Bottom half - scrollable summary
                yield FunctionSummaryWidget()

    def show_function(self, path: str, name: str) -> None:
        """Show details for the selected function."""
        details_container = self.query_one('#function-details')
        details = details_container.query_one(Static)
        summary_widget = self.query_one(FunctionSummaryWidget)
        metadata = get_function_metadata(path, name)

        if metadata['status'] == 'Available':
            sections: list[str] = []

            sections.extend([f"Path: {metadata['path']}", ''])

            sections.extend(['Source:', f"```rust\n{metadata['source']}\n```"])

            if metadata['doc']:
                sections.extend(['', 'Documentation:', metadata['doc']])

            markdown = Markdown('\n'.join(sections))
            details.update(markdown)

            summary_widget.generate_summary(
                metadata['signature'], metadata['doc'], metadata['source'], metadata['path']
            )
        else:
            details.update(f'Function {name} not found in {path}')
