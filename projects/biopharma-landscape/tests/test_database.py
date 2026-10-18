from pathlib import Path

from biopharma.models import Paper
from biopharma.storage.database import (
    get_papers,
    initialize_db,
    save_papers,
)


def test_paper_persistence_and_deduplication(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"

    initialize_db(db_path)

    paper = Paper(
        id="https://openalex.org/W123",
        title="Biological Foundation Models",
        doi=None,
        publication_date="2026-01-01",
        authors=["Jane Smith"],
        url="https://openalex.org/W123",
        source="openalex",
    )

    assert save_papers([paper], db_path) == 1
    assert save_papers([paper], db_path) == 0

    stored = get_papers(db_path)

    assert len(stored) == 1
    assert stored[0]["title"] == paper["title"]


def test_empty_database(tmp_path: Path) -> None:
    db_path = tmp_path / "empty.db"

    initialize_db(db_path)

    assert get_papers(db_path) == []
