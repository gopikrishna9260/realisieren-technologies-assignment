from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper


class QuotesScraper(BaseScraper):
    """
    Scraper for Quotes to Scrape.
    """

    START_URL = "https://quotes.toscrape.com/"

    def scrape(self):
        """
        Scrape all quotes by following pagination until
        there is no Next page.
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

            quote_items = soup.select("div.quote")

            self.logger.info(
                "Quotes page: %s | Quotes found: %d",
                current_url,
                len(quote_items),
            )

            for quote in quote_items:
                record = self.parse_quote(quote, current_url)

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
            "Quotes scraping completed. Total records: %d",
            len(records),
        )

        return records

    def parse_quote(self, quote, page_url):
        """
        Extract data from a single quote element.
        """

        text_element = quote.select_one("span.text")
        author_element = quote.select_one("small.author")

        if not text_element:
            self.logger.warning(
                "Quote skipped because text is missing."
            )
            return None

        quote_text = text_element.get_text(
            strip=True
        )

        author = (
            author_element.get_text(strip=True)
            if author_element
            else None
        )

        tags = [
            tag.get_text(strip=True)
            for tag in quote.select("a.tag")
        ]

        author_link_element = quote.select_one(
            'a[href^="/author/"]'
        )

        author_url = (
            urljoin(
                page_url,
                author_link_element["href"],
            )
            if author_link_element
            else None
        )

        return {
            "source": "quotes_to_scrape",
            "source_url": author_url,
            "name_or_title": quote_text,
            "category": None,
            "price": None,
            "rating": None,
            "author": author,
            "tags": tags,
            "description": None,
        }