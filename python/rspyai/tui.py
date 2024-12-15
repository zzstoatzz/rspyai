"""TUI for browsing Rust functions."""

from pathlib import Path
from typing import TypedDict

from rich.markdown import Markdown
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Input, Static, Tree

from rspyai import get_function_metadata, scan_rust_project
from rspyai.logging import get_logger

logger = get_logger(__name__)


class FunctionData(TypedDict):
    """Data for a function."""

    path: str
    name: str


class FunctionBrowser(App[None]):
    """A TUI for browsing Rust functions."""

    BINDINGS = [
        ('q', 'quit', 'Quit'),
        ('r', 'refresh', 'Rescan Project'),
    ]

    def __init__(self, root_path: str = '.'):
        """Initialize the FunctionBrowser."""
        super().__init__()
        self.root_path = root_path

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Horizontal():
            # Left panel: Function tree
            with Vertical(id='left-panel'):
                yield Input(placeholder='Search functions...', id='search')
                yield Tree('Functions', id='function-tree')

            # Right panel: Function details
            with Vertical(id='right-panel'):
                yield Static(id='function-details', expand=True)

        yield Footer()

    def on_mount(self) -> None:
        """Set up the initial state of the app."""
        self.scan_project()

    def scan_project(self) -> None:
        """Scan the Rust project for functions."""
        tree: Tree[FunctionData] = self.query_one('#function-tree', expect_type=Tree)
        tree.clear()

        # Group functions by file
        functions_by_file: dict[str, list[FunctionData]] = {}
        for func in scan_rust_project(self.root_path):
            path = func['path']
            if path not in functions_by_file:
                functions_by_file[path] = []
            functions_by_file[path].append({'path': func['path'], 'name': func['name']})

        # Add to tree grouped by file and expand
        for file_path, functions in functions_by_file.items():
            file_node = tree.root.add(Path(file_path).name, expand=True)  # Expand file nodes
            for func in functions:
                node = file_node.add(func['name'])
                node.data = FunctionData(path=func['path'], name=func['name'])

        tree.root.expand()  # Expand root node

    def _show_function_details(self, path: str, name: str) -> None:
        """Show details for the selected function."""
        details: Static = self.query_one('#function-details', expect_type=Static)
        metadata = get_function_metadata(path, name)

        if metadata['status'] == 'Available':
            markdown = Markdown(
                '\n'.join(
                    [
                        f"Path: {metadata['path']}",
                        '',
                        'Signature:',
                        f"```rust\n{metadata['signature']}\n```",
                        '',
                        'Documentation:',
                        metadata['doc'],
                    ]
                )
            )
            details.update(markdown)
        else:
            details.update(f'Function {name} not found in {path}')

    def on_tree_node_selected(self, event: Tree.NodeSelected[FunctionData]) -> None:
        """Handle selection of a function in the tree."""
        if metadata := event.node.data:
            self._show_function_details(metadata['path'], metadata['name'])

    def action_refresh(self) -> None:
        """Rescan the project directory."""
        self.scan_project()


def main():
    """App entrypoint."""
    import sys

    working_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    app = FunctionBrowser(working_dir)
    app.run()


if __name__ == '__main__':
    main()
