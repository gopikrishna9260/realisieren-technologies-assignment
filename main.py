import csv
import json
import logging
import time
from datetime import datetime
from pathlib import Path

from scrapers.books_scraper import BooksScraper
from scrapers.quotes_scraper import QuotesScraper

from processing.cleaning import clean_records
from processing.validation import validate_records
from processing.deduplication import deduplicate_records


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


CSV_FILE = OUTPUT_DIR / "final_dataset.csv"
JSON_FILE = OUTPUT_DIR / "summary_report.json"
LOG_FILE = LOG_DIR / "scraper.log"


# --------------------------------------------------
# Logging configuration
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        ),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# CSV columns
# --------------------------------------------------

FIELDNAMES = [
    "source",
    "source_url",
    "name_or_title",
    "category",
    "price",
    "rating",
    "author",
    "tags",
    "description",
    "scraped_at",
]


# --------------------------------------------------
# Main pipeline
# --------------------------------------------------

def main():

    start_time = datetime.now()

    logger.info("========================================")
    logger.info("Scraping assignment started")
    logger.info("========================================")

    raw_records = []
    raw_counts = {
        "books_to_scrape": 0,
        "quotes_to_scrape": 0,
    }

    rejected_records = []
    rejection_counts = {}

    duplicate_records = []

    # --------------------------------------------------
    # Step 1: Scrape Books
    # --------------------------------------------------

    try:

        logger.info("Starting Books to Scrape...")

        books_scraper = BooksScraper()

        books = books_scraper.scrape()

        books_scraper.close()

        raw_records.extend(books)

        raw_counts["books_to_scrape"] = len(books)

        logger.info(
            "Books scraping completed: %d records",
            len(books),
        )

    except Exception as error:

        logger.exception(
            "Books scraper failed: %s",
            error,
        )

    # --------------------------------------------------
    # Step 2: Scrape Quotes
    # --------------------------------------------------

    try:

        logger.info("Starting Quotes to Scrape...")

        quotes_scraper = QuotesScraper()

        quotes = quotes_scraper.scrape()

        quotes_scraper.close()

        raw_records.extend(quotes)

        raw_counts["quotes_to_scrape"] = len(quotes)

        logger.info(
            "Quotes scraping completed: %d records",
            len(quotes),
        )

    except Exception as error:

        logger.exception(
            "Quotes scraper failed: %s",
            error,
        )

    logger.info(
        "Total raw records: %d",
        len(raw_records),
    )

    # --------------------------------------------------
    # Step 3: Cleaning
    # --------------------------------------------------

    logger.info("Starting data cleaning...")

    cleaned_records = clean_records(raw_records)

    logger.info(
        "Cleaning completed: %d records",
        len(cleaned_records),
    )

    # --------------------------------------------------
    # Step 4: Add scraped timestamp
    # --------------------------------------------------

    scraped_at = datetime.now().isoformat()

    for record in cleaned_records:
        record["scraped_at"] = scraped_at

    # --------------------------------------------------
    # Step 5: Validation
    # --------------------------------------------------

    logger.info("Starting validation...")

    (
        valid_records,
        rejected_records,
        rejection_counts,
    ) = validate_records(cleaned_records)

    logger.info(
        "Validation completed. Valid: %d | Rejected: %d",
        len(valid_records),
        len(rejected_records),
    )

    for rejected in rejected_records:

        logger.warning(
            "Record rejected: %s",
            rejected["reason"],
        )

    # --------------------------------------------------
    # Step 6: Deduplication
    # --------------------------------------------------

    logger.info("Starting deduplication...")

    (
        unique_records,
        duplicate_records,
    ) = deduplicate_records(valid_records)

    logger.info(
        "Deduplication completed. Unique: %d | Duplicates: %d",
        len(unique_records),
        len(duplicate_records),
    )

    # --------------------------------------------------
    # Step 7: Write CSV
    # --------------------------------------------------

    logger.info(
        "Writing final dataset: %s",
        CSV_FILE,
    )

    with open(
        CSV_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=FIELDNAMES,
        )

        writer.writeheader()

        for record in unique_records:

            row = record.copy()

            # Store tags as JSON text inside CSV
            if isinstance(row.get("tags"), list):
                row["tags"] = json.dumps(
                    row["tags"],
                    ensure_ascii=False,
                )

            writer.writerow(row)

    # --------------------------------------------------
    # Step 8: Summary report
    # --------------------------------------------------

    end_time = datetime.now()

    duration = (
        end_time - start_time
    ).total_seconds()

    cleaned_counts = {
        "books_to_scrape": 0,
        "quotes_to_scrape": 0,
    }

    final_counts = {
        "books_to_scrape": 0,
        "quotes_to_scrape": 0,
    }

    for record in cleaned_records:

        source = record.get("source")

        if source in cleaned_counts:
            cleaned_counts[source] += 1

    for record in unique_records:

        source = record.get("source")

        if source in final_counts:
            final_counts[source] += 1

    summary = {
        "raw_records_per_source": raw_counts,

        "records_after_cleaning_per_source": cleaned_counts,

        "rejected_counts_by_reason": rejection_counts,

        "duplicates": len(duplicate_records),

        "final_record_count": len(unique_records),

        "final_records_per_source": final_counts,

        "start_time": start_time.isoformat(),

        "end_time": end_time.isoformat(),

        "duration_seconds": duration,
    }

    with open(
        JSON_FILE,
        "w",
        encoding="utf-8",
    ) as json_file:

        json.dump(
            summary,
            json_file,
            indent=4,
            ensure_ascii=False,
        )

    logger.info(
        "Summary report written: %s",
        JSON_FILE,
    )

    logger.info("========================================")
    logger.info("Pipeline completed successfully")
    logger.info(
        "Final records: %d",
        len(unique_records),
    )
    logger.info("========================================")


if __name__ == "__main__":
    main()