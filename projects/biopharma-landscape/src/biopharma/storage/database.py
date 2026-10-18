import json
import sqlite3
from pathlib import Path

DB_PATH = Path("data/biopharma.db")


def connect_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_db():
    with connect_db() as conn:
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


def save_papers(papers: list[dict]):
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


def get_papers() -> list[dict]:
    """Return all papers in the database."""
    with connect_db() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM papers ORDER BY publication_date DESC"
        ).fetchall()

    return [dict(row) for row in rows]
