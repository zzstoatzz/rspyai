"""Widget for displaying function details."""

from rich.markdown import Markdown
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static

from rspyai import get_function_metadata
from rspyai.widgets.function_summary import FunctionSummaryWidget


class FunctionDetails(Widget):
    """Widget for displaying function details."""

    def compose(self):
        """Create child widgets."""
        with Vertical():
            yield Static(id='function-details')
            yield FunctionSummaryWidget()

    def show_function(self, path: str, name: str) -> None:
        """Show details for the selected function."""
        details: Static = self.query_one('#function-details', expect_type=Static)
        summary_widget = self.query_one(FunctionSummaryWidget)
        metadata = get_function_metadata(path, name)

        if metadata['status'] == 'Available':
            markdown = Markdown(
                '\n'.join(
                    [
                        f"Path: {metadata['path']}",
                        '',
                        'Signature:',
                        '',
                        f"```rust\n{metadata['signature']}\n```",
                        '',
                        'Documentation:',
                        metadata['doc'],
                    ]
                )
            )
            details.update(markdown)

            # Start summary generation in background
            summary_widget.generate_summary(metadata['signature'], metadata['doc'], metadata['path'])
        else:
            details.update(f'Function {name} not found in {path}')
