from typing import List, final
import httpx

from textual import on
from textual.app import App, ComposeResult
from textual.reactive import reactive

from alexandria.app_header import AppHeader
from alexandria.book import Book
from alexandria.books_view import BooksView
from alexandria.footer import AppFooter
from alexandria.searchbar import SearchBar

class AlexandriaApp(App):
    """App to download digital books."""

    CSS_PATH = 'styles.tcss'

    books: reactive[List[Book]] = reactive([])
    loading_books: reactive[bool] = reactive(False)

    def __init__(self):
        super().__init__()
        self.title = 'Alexandria'
        self.sub_title = 'Search online books'

    @on(SearchBar.Submitted)
    async def search_books(self, event: SearchBar.Submitted):
        self.loading_books = True
        async with httpx.AsyncClient(timeout=20.0) as client:
            r = await client.get('http://localhost:8080/api/books?title=' + event.value)
            books = r.json()
            self.books = [Book.from_json(book) for book in books]
            self.query_one(SearchBar).clear()
            self.loading_books = False

    def compose(self) -> ComposeResult:
        yield AppHeader()
        yield SearchBar()
        yield (
            BooksView()
                .data_bind(AlexandriaApp.books)
                .data_bind(AlexandriaApp.loading_books)
        )
        # yield AppFooter()


if __name__ == "__main__":
    app = AlexandriaApp()
    app.run()
