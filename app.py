import json
from pathlib import Path

import streamlit as st

from main import main


st.set_page_config(
    page_title="Realisieren Technologies Assignment",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Python Web Scraping & Data Consolidation")
st.write(
    "Realisieren Technologies Pvt Ltd – Assignment"
)

st.markdown(
    """
    This application scrapes data from:

    - 📖 Books to Scrape
    - 💬 Quotes to Scrape

    It then performs cleaning, validation, deduplication,
    and generates the final consolidated dataset.
    """
)

if st.button("🚀 Run Scraping Pipeline", type="primary"):

    with st.spinner(
        "Scraping books and quotes... This may take around 2 minutes."
    ):
        try:
            main()

            st.success(
                "Scraping pipeline completed successfully!"
            )

        except Exception as error:
            st.error(
                f"Pipeline failed: {error}"
            )


summary_path = Path("output/summary_report.json")
csv_path = Path("output/final_dataset.csv")

if summary_path.exists():

    st.subheader("📊 Pipeline Summary")

    with open(summary_path, "r", encoding="utf-8") as file:
        summary = json.load(file)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Books",
        summary["raw_records_per_source"].get(
            "books_to_scrape", 0
        ),
    )

    col2.metric(
        "Quotes",
        summary["raw_records_per_source"].get(
            "quotes_to_scrape", 0
        ),
    )

    col3.metric(
        "Duplicates",
        summary["duplicates"],
    )

    col4.metric(
        "Final Records",
        summary["final_record_count"],
    )

    st.json(summary)


if csv_path.exists():

    st.subheader("📁 Final Dataset")

    with open(csv_path, "rb") as file:

        st.download_button(
            label="⬇️ Download final_dataset.csv",
            data=file,
            file_name="final_dataset.csv",
            mime="text/csv",
        )