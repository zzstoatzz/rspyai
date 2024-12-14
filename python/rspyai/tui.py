from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Input, Tree
import rspyai

class FunctionBrowser(App[None]):
    """A TUI for browsing Rust functions."""
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("f", "toggle_focus", "Toggle Focus"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Horizontal():
            # Left panel: Function tree
            with Vertical(id="left-panel"):
                yield Input(placeholder="Search functions...", id="search")
                yield Tree("Functions", id="function-tree")
            
            # Right panel: Function details
            with Vertical(id="right-panel"):
                yield Static(id="function-details", expand=True)
        
        yield Footer()

    def on_mount(self) -> None:
        """Set up the initial state of the app."""
        # Add example function to the tree
        tree: Tree[str] = self.query_one("#function-tree", expect_type=Tree[str])
        tree.root.add("sum_as_string")
        
        # Show initial function details
        details: Static = self.query_one("#function-details", expect_type=Static)
        details.update(rspyai.get_function_metadata("sum_as_string"))

    def on_tree_node_selected(self, event: Tree.NodeSelected[str]) -> None:
        """Handle selection of a function in the tree."""
        details: Static = self.query_one("#function-details", expect_type=Static)
        details.update(rspyai.get_function_metadata(event.node.label))

def main():
    app = FunctionBrowser()
    app.run()