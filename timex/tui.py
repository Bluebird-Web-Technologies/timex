from textual.app import App
from textual.containers import VerticalScroll
from textual.widgets import Footer
from textual.widgets import Markdown

WELCOME = """\
# Welcome to Timex!

Your _simple_, _minimalist_ project time sheet
"""


class Content(VerticalScroll, can_focus=False):
    """Non focusable vertical scroll."""


class HomeScreen(App):
    def compose(self):
        with Content():
            yield Markdown(WELCOME)
        yield Footer()
