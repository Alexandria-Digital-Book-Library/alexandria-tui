from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Footer


class AppFooter(Widget):
    def compose(self) -> ComposeResult:
        yield Footer()
