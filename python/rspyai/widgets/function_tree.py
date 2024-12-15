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

        # Group functions by file
        functions_by_file: dict[str, list[FunctionData]] = {}
        for func in scan_rust_project(self.root_path):
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
