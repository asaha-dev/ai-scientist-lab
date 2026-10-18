import json
import sqlite3
from collections.abc import Generator
from contextlib import closing, contextmanager
from pathlib import Path
from typing import Any

from biopharma.models import Paper

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "biopharma.db"


@contextmanager
def connect_db(
    db_path: Path = DEFAULT_DB_PATH,
) -> Generator[sqlite3.Connection, None, None]:
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with closing(sqlite3.connect(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        with conn:
            yield conn


def initialize_db(db_path: Path = DEFAULT_DB_PATH) -> None:
    with connect_db(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS papers (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                doi TEXT,
                publication_date TEXT,
                authors TEXT,
                url TEXT,
                source TEXT,
                ingested_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_papers(
    papers: list[Paper],
    db_path: Path = DEFAULT_DB_PATH,
) -> int:
    """Insert new papers; ignore previously ingested papers."""
    # TODO: Can update papers if they have changed since last ingestion, but for now we just ignore them.
    with connect_db() as conn:
        before = conn.total_changes

        for paper in papers:
            conn.execute(
                """
                INSERT OR IGNORE INTO papers
                (id, title, doi, publication_date,
                 authors, url, source)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    paper["id"],
                    paper["title"],
                    paper.get("doi"),
                    paper.get("publication_date"),
                    json.dumps(paper.get("authors", [])),
                    paper.get("url"),
                    paper.get("source"),
                ),
            )
        return conn.total_changes - before


def get_papers(
    db_path: Path = DEFAULT_DB_PATH,
) -> list[dict[str, Any]]:
    """Return all papers in the database."""
    with connect_db() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM papers ORDER BY publication_date DESC"
        ).fetchall()

    return [dict(row) for row in rows]
