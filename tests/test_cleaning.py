from processing.cleaning import (
    clean_text,
    clean_price,
    clean_rating,
    clean_tags,
    clean_url,
)


def test_clean_text():
    assert clean_text("  Hello   World  ") == "Hello World"


def test_clean_price():
    assert clean_price("£51.77") == 51.77
    assert clean_price("Â£51.77") == 51.77


def test_clean_rating():
    assert clean_rating("Five") == 5
    assert clean_rating("Three") == 3
    assert clean_rating(4) == 4


def test_clean_tags():
    result = clean_tags(["  Python ", " AWS  "])

    assert result == ["Python", "AWS"]


def test_clean_url():
    assert (
        clean_url(" https://example.com ")
        == "https://example.com"
    )

    assert clean_url("not-a-url") is None