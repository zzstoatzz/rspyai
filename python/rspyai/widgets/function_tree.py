"""Function tree widget for the TUI."""

from collections.abc import Generator
from pathlib import Path
from typing import Any, Self, TypedDict

from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Input, Tree

from rspyai import scan_rust_project
from rspyai.logging import get_logger

logger = get_logger(__name__)


class FunctionData(TypedDict):
    """Data for a function."""

    path: str
    name: str


class FunctionTree(Widget):
    """Widget for displaying and searching Rust functions."""

    def __init__(self):
        """Initialize the widget."""
        super().__init__()
        self.root_path = '.'
        self._tree: Tree[FunctionData] | None = None

    def compose(self: Self) -> Generator[Input | Tree[FunctionData], Any, None]:
        """Create child widgets."""
        with Vertical():
            yield Input(placeholder='Search functions...', id='search')
            self._tree = Tree('Functions', id='function-tree')
            yield self._tree

    def on_mount(self) -> None:
        """Initialize the tree on mount."""
        self.scan_project()

    def scan_project(self, root_path: str | None = None) -> None:
        """Scan the Rust project for functions."""
        if root_path is not None:
            self.root_path = root_path

        if not self._tree:
            logger.debug('Tree not initialized yet')
            return

        logger.debug(f'Scanning project at {self.root_path}')
        self._tree.clear()

        functions = scan_rust_project(self.root_path)

        if not functions:
            self._tree.root.add(f'no rust functions found in {self.root_path}')
            return

        # Group functions by file
        functions_by_file: dict[str, list[FunctionData]] = {}
        for func in functions:
            path = func['path']
            if path not in functions_by_file:
                functions_by_file[path] = []
            functions_by_file[path].append({'path': func['path'], 'name': func['name']})

        # Add to tree grouped by file and expand
        for file_path, functions in functions_by_file.items():
            file_node = self._tree.root.add(Path(file_path).name, expand=True)
            for func in functions:
                node = file_node.add(func['name'])
                node.data = FunctionData(path=func['path'], name=func['name'])

        self._tree.root.expand()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes."""
        search_term = event.value.lower()

        # Skip if tree isn't initialized
        if not self._tree:
            return

        # Show all items if search is empty
        if not search_term:
            for file_node in self._tree.root.children:
                file_node.display = True
                file_node.collapse()
                for func_node in file_node.children:
                    func_node.display = True
            return

        # Walk through all nodes and hide/show based on search
        for file_node in self._tree.root.children:
            has_matches = False
            file_node.display = True

            # Check function nodes
            for func_node in file_node.children:
                matches = search_term in str(func_node.label).lower()
                func_node.display = matches
                has_matches = has_matches or matches

            # Expand file node if it has matches, collapse if not
            if has_matches:
                file_node.expand()
            else:
                file_node.collapse()
