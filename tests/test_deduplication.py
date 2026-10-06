from processing.deduplication import (
    create_fingerprint,
    deduplicate_records,
)


def test_book_duplicate():

    records = [
        {
            "source": "books_to_scrape",
            "name_or_title": "The Great Book",
        },
        {
            "source": "books_to_scrape",
            "name_or_title": "The Great Book",
        },
    ]

    unique, duplicates = deduplicate_records(records)

    assert len(unique) == 1
    assert len(duplicates) == 1


def test_quote_duplicate():

    records = [
        {
            "source": "quotes_to_scrape",
            "author": "Albert Einstein",
            "name_or_title": "The world as we have created it.",
        },
        {
            "source": "quotes_to_scrape",
            "author": "Albert Einstein",
            "name_or_title": "The world as we have created it.",
        },
    ]

    unique, duplicates = deduplicate_records(records)

    assert len(unique) == 1
    assert len(duplicates) == 1


def test_different_books_are_not_duplicates():

    records = [
        {
            "source": "books_to_scrape",
            "name_or_title": "Book One",
        },
        {
            "source": "books_to_scrape",
            "name_or_title": "Book Two",
        },
    ]

    unique, duplicates = deduplicate_records(records)

    assert len(unique) == 2
    assert len(duplicates) == 0


def test_fingerprint_is_generated():

    record = {
        "source": "books_to_scrape",
        "name_or_title": "Test Book",
    }

    fingerprint = create_fingerprint(record)

    assert isinstance(fingerprint, str)
    assert len(fingerprint) == 64