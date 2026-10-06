import hashlib
import re


def normalize_text(value):
    """
    Normalize text for duplicate detection.
    """

    if value is None:
        return ""

    value = str(value).lower()

    # Remove punctuation
    value = re.sub(r"[^\w\s]", "", value)

    # Collapse multiple spaces
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def create_fingerprint(record):
    """
    Create a unique fingerprint for a record.

    Books:
        source + title

    Quotes:
        source + author + first 50 characters of quote
    """

    source = normalize_text(
        record.get("source")
    )

    if source == "books_to_scrape":

        title = normalize_text(
            record.get("name_or_title")
        )

        fingerprint_text = (
            f"{source}|{title}"
        )

    elif source == "quotes_to_scrape":

        author = normalize_text(
            record.get("author")
        )

        quote = normalize_text(
            record.get("name_or_title")
        )[:50]

        fingerprint_text = (
            f"{source}|{author}|{quote}"
        )

    else:

        fingerprint_text = (
            f"{source}|"
            f"{normalize_text(record.get('name_or_title'))}"
        )

    return hashlib.sha256(
        fingerprint_text.encode("utf-8")
    ).hexdigest()


def deduplicate_records(records):
    """
    Remove duplicate records.

    Returns:
        unique_records,
        duplicate_records
    """

    seen = set()

    unique_records = []
    duplicate_records = []

    for record in records:

        fingerprint = create_fingerprint(record)

        if fingerprint in seen:

            duplicate_records.append(
                {
                    "record": record,
                    "fingerprint": fingerprint,
                }
            )

        else:

            seen.add(fingerprint)
            unique_records.append(record)

    return unique_records, duplicate_records