import os

import httpx

OPENALEX_API_URL = "https://api.openalex.org/works"


def search_papers(
    query: str,
    limit: int = 20,
) -> list[dict]:
    """
    Search for papers using the OpenAlex API.

    Args:
        query (str): The search query.
        limit (int): The maximum number of results to return.

    Returns:
        list[dict]: A list of papers matching the search query.
    """
    params = {
        "search": query,
        "per_page": limit,
        "sort": "publication_date:desc",
    }

    api_key = os.getenv("OPENALEX_API_KEY")
    if api_key:
        params["api_key"] = api_key

    with httpx.Client(timeout=30.0) as client:
        response = client.get(OPENALEX_API_URL, params=params)
        response.raise_for_status()
        results = response.json()["results"]
        return [normalize_paper(paper) for paper in results]


def normalize_paper(paper: dict) -> dict:
    """
    Convert OpenAlex records to our internal schema."""

    authors = [
        item["author"]["display_name"]
        for item in paper.get("authorships", [])
        if item.get("author")
    ]

    return {
        "id": paper.get("id"),
        "title": paper.get("title"),
        "doi": paper.get("doi"),
        "publication_date": paper.get("publication_date"),
        "authors": authors,
        "url": (
            paper.get("doi")
            or paper.get("primary_location", {}).get("landing_page_url")
            if paper.get("primary_location") is not None
            else paper.get("doi")
        )
        or paper["id"],
        "source": "openalex",
    }
