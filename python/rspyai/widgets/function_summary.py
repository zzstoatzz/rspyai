"""Widget for displaying AI-generated function summaries."""

from pydantic_ai import Agent
from rich.console import Console, ConsoleOptions, RenderResult
from rich.markdown import CodeBlock, Markdown
from rich.syntax import Syntax
from rich.text import Text
from textual import work
from textual.containers import VerticalScroll
from textual.widget import Widget
from textual.widgets import Static


class SimpleCodeBlock(CodeBlock):
    """Prettier code blocks for markdown."""

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        """Render the code block."""
        code = str(self.text).rstrip()
        yield Text(self.lexer_name, style='dim')
        yield Syntax(
            code,
            self.lexer_name,
            theme=self.theme,
            background_color='default',
            word_wrap=True,
        )
        yield Text(f'/{self.lexer_name}', style='dim')


# Use prettier code blocks
Markdown.elements['fence'] = SimpleCodeBlock


class FunctionSummaryWidget(Widget):
    """Widget for displaying AI-generated function summaries."""

    def __init__(self):
        """Initialize the widget."""
        super().__init__()
        self._current_task: str | None = None

    @property
    def summary_agent(self) -> Agent[None, str]:
        """Get the agent."""
        return Agent(
            'openai:gpt-4o',
            result_type=str,
            system_prompt=(
                'You are hyper-concise and dry Marvin, the paranoid android. '
                'Dryly summarize the function in a few phrases. '
                'Use `inline code` syntax when referring to specific parts of the code. '
            ),
        )

    def compose(self):
        """Create child widgets."""
        with VerticalScroll(id='summary-scroll'):
            yield Static(id='function-summary', expand=True)

    @work(thread=True)
    async def generate_summary(self, signature: str, docs: str) -> None:
        """Generate and display a summary for the function."""
        task_id = f'{signature}:{docs}'
        self._current_task = task_id

        summary_view = self.query_one('#function-summary', expect_type=Static)
        summary_view.update(Markdown('*Here I am, brain the size of a planet, analyzing your code...*'))

        prompt = f"""
        Analyze this depressingly simple Rust function:

        ```rust
        {signature}
        ```

        Documentation (if you can call it that):
        {docs}
        """

        try:
            async with self.summary_agent.run_stream(prompt) as result:
                async for message in result.stream():
                    if self._current_task != task_id:
                        return
                    summary_view.update(Markdown(message))
                    summary_view.scroll_visible()

        except Exception as e:
            if self._current_task == task_id:
                summary_view.update(
                    Markdown("*Failed to generate summary. Not that I'm surprised.* " f"Here's why: {str(e)}")
                )
