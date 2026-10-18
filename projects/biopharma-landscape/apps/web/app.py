import json

import pandas as pd
import streamlit as st

from biopharma.ingestion.openalex import search_papers
from biopharma.storage.database import get_papers, save_papers

st.set_page_config(page_title="Biopharma AI Observatory", layout="wide")
st.caption("Scientific research • Emerging AI • Biopharma")

st.subheader("Paper Radar")

query = st.text_input(
    "Research topic",
    value="biological foundation models",
)

if st.button("Discover papers"):
    try:
        with st.spinner("Searching OpenAlex..."):
            papers = search_papers(query, limit=25)
            added = save_papers(papers)

        st.success(
            f"Retrieved {len(papers)} records. Added {added} new papers."
        )
    except Exception as exc:
        st.error(f"Paper discovery failed: {exc}")

papers = get_papers()

if papers:
    df = pd.DataFrame(papers)

    df["authors"] = df["authors"].apply(lambda x: ", ".join(json.loads(x)[:3]))

    st.metric("Papers in local library", len(df))

    st.dataframe(
        df[["publication_date", "title", "authors", "url"]],
        column_config={
            "publication_date": "Published",
            "title": "Paper",
            "authors": "Authors",
            "url": st.column_config.LinkColumn("Source"),
        },
        hide_index=True,
        use_container_width=True,
    )
else:
    st.info("Discover papers to populate the research library.")
