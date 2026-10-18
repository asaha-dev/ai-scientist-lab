from typing import TypedDict


class Paper(TypedDict):
    """Normalized publication metadata used by the application."""

    id: str
    title: str
    doi: str | None
    publication_date: str | None
    authors: list[str]
    url: str
    source: str
