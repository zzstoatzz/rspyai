"""Widget for displaying AI-generated function summaries."""

from pydantic_ai import Agent
from rich.console import Console, ConsoleOptions, RenderResult
from rich.markdown import CodeBlock, Markdown
from rich.syntax import Syntax
from textual import work
from textual.containers import VerticalScroll
from textual.widget import Widget
from textual.widgets import Static

from rspyai.settings import get_settings


class SimpleCodeBlock(CodeBlock):
    """Prettier code blocks for markdown."""

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        """Render the code block."""
        code = str(self.text).rstrip()
        yield Syntax(
            code,
            self.lexer_name,
            theme=self.theme,
            background_color='default',
            word_wrap=True,
        )


# Use prettier code blocks
Markdown.elements['fence'] = SimpleCodeBlock


class FunctionSummaryWidget(Widget):
    """Widget for displaying AI-generated function summaries."""

    def __init__(self):
        """Initialize the widget."""
        super().__init__()
        self._current_task: str | None = None
        self._message_cache: dict[str, str] = {}

    @property
    def summary_agent(self) -> Agent[None, str]:
        """Get the agent."""
        settings = get_settings()
        return Agent(
            settings.ai_model,
            system_prompt=settings.ai_system_prompt,
        )

    @property
    def default_loading_message(self) -> str:
        """Get the default loading message."""
        settings = get_settings()
        return settings.default_loading_message

    def compose(self):
        """Create child widgets."""
        with VerticalScroll(id='summary-scroll'):
            yield Static(id='function-summary', expand=True)

    @work(thread=True)
    async def generate_summary(self, signature: str, docs: str, source: str, file_path: str) -> None:
        """Generate and display a summary for the function.

        Args:
            signature: The function signature
            docs: The function documentation
            source: The function source code
            file_path: The absolute path to the source file
        """
        # Include file_path in the cache key to avoid collisions
        task_id = f'{file_path}:{signature}:{docs}'
        self._current_task = task_id

        summary_view = self.query_one('#function-summary', expect_type=Static)

        # Check cache first
        if cached_message := self._message_cache.get(task_id):
            summary_view.update(Markdown(cached_message))
            summary_view.scroll_visible()
            return

        summary_view.update(Markdown(self.default_loading_message))

        prompt = f"""
        Analyze this Rust function from {file_path}:

        Source code:
        ```rust
        {source}
        ```

        {f"Documentation:\n{docs}" if docs else ''}
        """

        try:
            async with self.summary_agent.run_stream(prompt) as result:
                final_message = ''
                async for message in result.stream():
                    if self._current_task != task_id:
                        return
                    final_message = message
                    summary_view.update(Markdown(message))
                    summary_view.scroll_visible()

                # Cache the final message
                self._message_cache[task_id] = final_message

        except Exception as e:
            if self._current_task == task_id:
                error_message = f'*Failed to generate summary* {str(e)}'
                summary_view.update(Markdown(error_message))
                self._message_cache[task_id] = error_message
