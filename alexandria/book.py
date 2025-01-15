from dataclasses import dataclass
from typing import Literal, List


BookExtension = Literal["PDF", "EPUB", "AZW3", "MOBI"]


@dataclass
class Book:
    title: str
    authors: List[str]
    extension: BookExtension
    size: str
    image_url: str
    download_url: str
    should_open_browser: bool

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            title=data['title'],
            authors=data['authors'],
            extension=data['extension'],
            size=data['size'],
            image_url=data['imageUrl'],
            download_url=data['downloadUrl'],
            should_open_browser=data['shouldOpenBrowser']
        )
