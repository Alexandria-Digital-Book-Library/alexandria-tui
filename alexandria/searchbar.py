from textual.widgets import Input


class SearchBar(Input):
    def __init__(self):
        super().__init__(
            placeholder="Enter a book",
            validate_on=["submitted"],
        )
