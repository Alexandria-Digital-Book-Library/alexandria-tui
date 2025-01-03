

from textual import screen
from textual.widgets import Header


class AppHeader(Header):
    def __init__(self):
        super().__init__()
        self.tall = True
        self.icon = '📖'
