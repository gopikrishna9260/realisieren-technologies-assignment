from urllib.parse import urlparse


VALID_SOURCES = {
    "books_to_scrape",
    "quotes_to_scrape",
}


def is_valid_url(url):
    """
    Check whether a URL looks valid.
    """

    if not url:
        return False

    try:
        parsed = urlparse(url)

        return (
            parsed.scheme in {"http", "https"}
            and bool(parsed.netloc)
        )

    except Exception:
        return False


def validate_record(record):
    """
    Validate one cleaned record.

    Returns:
        (True, None) if valid
        (False, reason) if invalid
    """

    # Check source
    source = record.get("source")

    if source not in VALID_SOURCES:
        return False, "invalid_source"

    # Check source URL
    source_url = record.get("source_url")

    if not is_valid_url(source_url):
        return False, "invalid_source_url"

    # Check title / quote text
    name_or_title = record.get("name_or_title")

    if not name_or_title:
        return False, "missing_name_or_title"

    # Validate books
    if source == "books_to_scrape":

        price = record.get("price")

        if price is not None:
            if not isinstance(price, (int, float)):
                return False, "invalid_price"

            if price < 0:
                return False, "invalid_price"

        rating = record.get("rating")

        if rating is not None:
            if not isinstance(rating, int):
                return False, "invalid_rating"

            if not 1 <= rating <= 5:
                return False, "invalid_rating"

    # Validate quotes
    elif source == "quotes_to_scrape":

        author = record.get("author")

        if not author:
            return False, "missing_author"

    return True, None


def validate_records(records):
    """
    Validate all records.

    Returns:
        valid_records,
        rejected_records,
        rejection_counts
    """

    valid_records = []
    rejected_records = []
    rejection_counts = {}

    for record in records:

        is_valid, reason = validate_record(record)

        if is_valid:
            valid_records.append(record)

        else:
            rejected_records.append(
                {
                    "record": record,
                    "reason": reason,
                }
            )

            rejection_counts[reason] = (
                rejection_counts.get(reason, 0) + 1
            )

    return (
        valid_records,
        rejected_records,
        rejection_counts,
    )