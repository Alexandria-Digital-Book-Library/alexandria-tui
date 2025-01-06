from typing import List
from importlib import resources
from pathlib import Path
import httpx

from textual import on, work
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Static, LoadingIndicator
from textual.containers import Vertical

from alexandria.app_header import AppHeader
from alexandria.book import Book
from alexandria.books_view import BooksView
from alexandria.footer import AppFooter
from alexandria.searchbar import SearchBar


class AlexandriaApp(App):
    """App to download digital books."""
    books: reactive[List[Book]] = reactive([], recompose=True)
    loading_books: reactive[bool] = reactive(False, recompose=True)

    def __init__(self):
        self.CSS_PATH = self._get_css_path()
        super().__init__()
        self.title = "Alexandria"
        self.sub_title = "Search books online"

    def _get_css_path(self):
        try:
            with resources.path('alexandria.assets', 'styles.css') as path:
                return path
        except Exception as _:
            return Path(__file__).parent / "../assets/styles.tcss"

    @on(SearchBar.Submitted)
    async def handle_search_bar_submitted(self, event: SearchBar.Submitted):
        event.stop()
        self.search_books(event.value)

    @work
    async def search_books(self, title: str):
        self.loading_books = True
        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                r = await client.get(f"http://localhost:8080/api/books?title={title}")
                if r.status_code == 200:
                    books = r.json()
                    self.books = [Book.from_json(book) for book in books]
                    self.query_one(SearchBar).clear()
                elif r.status_code == 400:
                    error = r.json()
                    self.notify(error["error"],
                                title="Error", severity="error")
        except:
            self.notify(
                "There was a problem fetching results\nPlease, try again later",
                title="Error",
                severity="error",
            )
        finally:
            self.loading_books = False

    def compose(self) -> ComposeResult:
        yield AppHeader()
        yield SearchBar()

        if self.loading_books:
            with Vertical(id="search-books-loading-indicator"):
                yield Static("Searching books")
                yield LoadingIndicator()
        elif len(self.books) > 0:
            yield BooksView().data_bind(AlexandriaApp.books)
        else:
            with Vertical(id="empty-books"):
                yield Static("Wow, such empty!")
                yield Static("Use the search bar to start looking for books")

        yield AppFooter()
