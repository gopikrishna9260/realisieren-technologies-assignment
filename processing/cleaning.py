import re


RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def clean_text(value):
    """
    Remove extra whitespace and normalize text.
    """

    if value is None:
        return None

    value = str(value)

    # Replace non-breaking spaces
    value = value.replace("\xa0", " ")

    # Remove extra whitespace
    value = re.sub(r"\s+", " ", value)

    value = value.strip()

    return value if value else None


def clean_price(value):
    """
    Convert book price such as:
    '£51.77' or 'Â£51.77'
    into:
    51.77
    """

    if value is None:
        return None

    value = str(value)

    # Fix common encoding artifact
    value = value.replace("Â£", "")
    value = value.replace("£", "")

    # Remove any remaining non-numeric characters
    value = re.sub(r"[^0-9.]", "", value)

    if not value:
        return None

    try:
        return float(value)
    except ValueError:
        return None


def clean_rating(value):
    """
    Convert rating values into integers from 1 to 5.
    """

    if value is None:
        return None

    if isinstance(value, int):
        return value if 1 <= value <= 5 else None

    value = clean_text(value)

    if value is None:
        return None

    if value in RATING_MAP:
        return RATING_MAP[value]

    try:
        rating = int(value)

        if 1 <= rating <= 5:
            return rating

    except ValueError:
        pass

    return None


def clean_tags(value):
    """
    Clean quote tags and return them as a list.
    """

    if value is None:
        return None

    if isinstance(value, str):
        value = [value]

    cleaned_tags = []

    for tag in value:
        cleaned_tag = clean_text(tag)

        if cleaned_tag:
            cleaned_tags.append(cleaned_tag)

    return cleaned_tags if cleaned_tags else None


def clean_url(value):
    """
    Basic URL cleaning.
    """

    if value is None:
        return None

    value = clean_text(value)

    if value and (
        value.startswith("http://")
        or value.startswith("https://")
    ):
        return value

    return None


def clean_record(record):
    """
    Clean one scraped record.
    """

    cleaned = dict(record)

    cleaned["source"] = clean_text(
        cleaned.get("source")
    )

    cleaned["source_url"] = clean_url(
        cleaned.get("source_url")
    )

    cleaned["name_or_title"] = clean_text(
        cleaned.get("name_or_title")
    )

    cleaned["category"] = clean_text(
        cleaned.get("category")
    )

    cleaned["price"] = clean_price(
        cleaned.get("price")
    )

    cleaned["rating"] = clean_rating(
        cleaned.get("rating")
    )

    cleaned["author"] = clean_text(
        cleaned.get("author")
    )

    cleaned["tags"] = clean_tags(
        cleaned.get("tags")
    )

    cleaned["description"] = clean_text(
        cleaned.get("description")
    )

    return cleaned


def clean_records(records):
    """
    Clean all scraped records.
    """

    return [
        clean_record(record)
        for record in records
    ]