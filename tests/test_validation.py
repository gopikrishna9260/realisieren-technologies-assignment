from processing.validation import validate_record


def test_valid_book():
    record = {
        "source": "books_to_scrape",
        "source_url": "https://books.toscrape.com/book",
        "name_or_title": "Test Book",
        "category": None,
        "price": 25.50,
        "rating": 4,
        "author": None,
        "tags": None,
        "description": None,
    }

    is_valid, reason = validate_record(record)

    assert is_valid is True
    assert reason is None


def test_invalid_book_rating():
    record = {
        "source": "books_to_scrape",
        "source_url": "https://books.toscrape.com/book",
        "name_or_title": "Test Book",
        "category": None,
        "price": 25.50,
        "rating": 6,
        "author": None,
        "tags": None,
        "description": None,
    }

    is_valid, reason = validate_record(record)

    assert is_valid is False
    assert reason == "invalid_rating"


def test_invalid_book_price():
    record = {
        "source": "books_to_scrape",
        "source_url": "https://books.toscrape.com/book",
        "name_or_title": "Test Book",
        "category": None,
        "price": -10,
        "rating": 4,
        "author": None,
        "tags": None,
        "description": None,
    }

    is_valid, reason = validate_record(record)

    assert is_valid is False
    assert reason == "invalid_price"


def test_valid_quote():
    record = {
        "source": "quotes_to_scrape",
        "source_url": "https://quotes.toscrape.com/author/test",
        "name_or_title": "This is a test quote.",
        "category": None,
        "price": None,
        "rating": None,
        "author": "Test Author",
        "tags": ["test"],
        "description": None,
    }

    is_valid, reason = validate_record(record)

    assert is_valid is True
    assert reason is None


def test_quote_missing_author():
    record = {
        "source": "quotes_to_scrape",
        "source_url": "https://quotes.toscrape.com/author/test",
        "name_or_title": "This is a test quote.",
        "category": None,
        "price": None,
        "rating": None,
        "author": None,
        "tags": ["test"],
        "description": None,
    }

    is_valid, reason = validate_record(record)

    assert is_valid is False
    assert reason == "missing_author"