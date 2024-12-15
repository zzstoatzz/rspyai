"""TUI for browsing Rust functions."""

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Header, Tree

from rspyai.settings import get_settings
from rspyai.widgets.function_details import FunctionDetails
from rspyai.widgets.function_tree import FunctionData, FunctionTree


class FunctionBrowser(App[None]):
    """A TUI for browsing Rust functions."""

    BINDINGS = [
        ('q', 'quit', 'Quit'),
        ('r', 'refresh', 'Rescan Project'),
    ]

    CSS = """
    FunctionTree {
        width: 33%;
        border: solid $primary;
        background: $surface;
    }

    FunctionDetails {
        width: 1fr;
        margin-left: 1;
        height: 100%;
    }

    #function-details {
        height: 1fr;
        background: $surface;
        padding: 1;
        overflow-y: auto;
    }

    #summary-scroll {
        height: 1fr;
        background: $surface;
        padding: 1;
        overflow-y: auto;
    }

    #function-summary {
        width: 100%;
        height: auto;
    }

    Input {
        margin: 1;
    }

    Tree {
        padding: 1;
    }

    Tree > .tree--guides {
        border-right: solid $primary;
    }
    """

    def __init__(self, root_path: str = '.'):
        """Initialize the FunctionBrowser."""
        super().__init__()
        self.root_path = root_path
        self.settings = get_settings()

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        with Horizontal():
            tree = FunctionTree()
            tree.scan_project(self.root_path)
            yield tree
            yield FunctionDetails()
        yield Footer()

    def on_tree_node_selected(self, event: Tree.NodeSelected[FunctionData]) -> None:
        """Handle selection of a function in the tree."""
        if metadata := event.node.data:
            details = self.query_one(FunctionDetails)
            details.show_function(metadata['path'], metadata['name'])

    def action_refresh(self) -> None:
        """Rescan the project directory."""
        tree = self.query_one(FunctionTree)
        tree.scan_project(self.root_path)


def main():
    """App entrypoint."""
    import sys

    working_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    app = FunctionBrowser(working_dir)
    app.run()


if __name__ == '__main__':
    main()
