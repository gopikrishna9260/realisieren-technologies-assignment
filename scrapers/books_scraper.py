from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper


class BooksScraper(BaseScraper):
    """
    Scraper for Books to Scrape.
    """

    START_URL = "https://books.toscrape.com/"

    RATING_MAP = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
    }

    def scrape(self):
        """
        Scrape all books by following pagination until there is no Next page.
        """

        records = []
        current_url = self.START_URL

        while current_url:
            response = self.fetch(current_url)

            if response is None:
                self.logger.error(
                    "Skipping page because request failed: %s",
                    current_url,
                )
                break

            soup = BeautifulSoup(response.text, "lxml")

            book_items = soup.select("article.product_pod")

            self.logger.info(
                "Books page: %s | Books found: %d",
                current_url,
                len(book_items),
            )

            for book in book_items:
                record = self.parse_book(book, current_url)

                if record:
                    records.append(record)

            next_link = soup.select_one("li.next > a")

            if next_link and next_link.get("href"):
                current_url = urljoin(
                    current_url,
                    next_link["href"],
                )
            else:
                current_url = None

        self.logger.info(
            "Books scraping completed. Total records: %d",
            len(records),
        )

        return records

    def parse_book(self, book, page_url):
        """
        Extract data from a single book element.
        """

        title_element = book.select_one("h3 > a")
        price_element = book.select_one("p.price_color")
        rating_element = book.select_one("p.star-rating")

        if not title_element:
            self.logger.warning(
                "Book skipped because title is missing."
            )
            return None

        title = title_element.get("title", "").strip()

        price = (
            price_element.get_text(strip=True)
            if price_element
            else None
        )

        rating = None

        if rating_element:
            rating_classes = rating_element.get("class", [])

            for class_name in rating_classes:
                if class_name in self.RATING_MAP:
                    rating = self.RATING_MAP[class_name]
                    break

        relative_url = title_element.get("href")

        book_url = (
            urljoin(page_url, relative_url)
            if relative_url
            else None
        )

        return {
            "source": "books_to_scrape",
            "source_url": book_url,
            "name_or_title": title,
            "category": None,
            "price": price,
            "rating": rating,
            "author": None,
            "tags": None,
            "description": None,
        }