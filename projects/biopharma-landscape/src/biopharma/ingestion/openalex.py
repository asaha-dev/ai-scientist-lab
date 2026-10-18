"""Retrieve and normalize publication metadata from OpenAlex."""

import os
from typing import Any

import httpx

from biopharma.models import Paper

OPENALEX_URL = "https://api.openalex.org/works"


def normalize_paper(record: dict[str, Any]) -> Paper:
    """Convert an OpenAlex work into our internal paper schema."""

    paper_id = record["id"]

    authors = [
        authorship["author"]["display_name"]
        for authorship in record.get("authorships", [])
        if authorship.get("author", {}).get("display_name")
    ]

    primary_location = record.get("primary_location") or {}

    url = (
        record.get("doi")
        or primary_location.get("landing_page_url")
        or paper_id
    )

    return Paper(
        id=paper_id,
        title=record.get("display_name") or "",
        doi=record.get("doi"),
        publication_date=record.get("publication_date"),
        authors=authors,
        url=url,
        source="openalex",
    )


def search_papers(
    query: str,
    limit: int = 20,
    *,
    client: httpx.Client | None = None,
) -> list[Paper]:
    """Search OpenAlex and return normalized publication metadata."""

    if not query.strip():
        raise ValueError("Search query cannot be empty")

    if not 1 <= limit <= 200:
        raise ValueError("Limit must be between 1 and 200")

    params = {
        "search": query,
        "per_page": limit,
        "sort": "publication_date:desc",
    }

    api_key = os.getenv("OPENALEX_API_KEY")
    if api_key:
        params["api_key"] = api_key

    def fetch(active_client: httpx.Client) -> list[Paper]:
        response = active_client.get(OPENALEX_URL, params=params)
        response.raise_for_status()

        results = response.json()["results"]

        if not isinstance(results, list):
            raise ValueError(
                "Unexpected OpenAlex response: results is not a list"
            )

        return [normalize_paper(record) for record in results]

    if client is not None:
        return fetch(client)

    with httpx.Client(timeout=30.0) as new_client:
        return fetch(new_client)
