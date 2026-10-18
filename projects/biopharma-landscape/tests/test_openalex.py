import httpx
import pytest

from biopharma.ingestion.openalex import normalize_paper, search_papers


def test_normalize_paper() -> None:
    record = {
        "id": "https://openalex.org/W123",
        "display_name": "A Biological Foundation Model",
        "doi": "https://doi.org/10.1234/example",
        "publication_date": "2026-01-01",
        "authorships": [
            {"author": {"display_name": "Jane Smith"}},
        ],
        "primary_location": None,
    }

    paper = normalize_paper(record)

    assert paper["id"] == "https://openalex.org/W123"
    assert paper["title"] == "A Biological Foundation Model"
    assert paper["authors"] == ["Jane Smith"]
    assert paper["source"] == "openalex"


def test_search_papers_with_mock_api() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["search"] == "protein models"

        return httpx.Response(
            200,
            json={
                "results": [
                    {
                        "id": "https://openalex.org/W123",
                        "display_name": "Protein Foundation Models",
                    }
                ]
            },
        )

    transport = httpx.MockTransport(handler)

    with httpx.Client(transport=transport) as client:
        papers = search_papers("protein models", client=client)

    assert len(papers) == 1
    assert papers[0]["title"] == "Protein Foundation Models"


def test_empty_query_is_rejected() -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        search_papers("  ")
