import logging
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseScraper:
    """
    Common HTTP functionality shared by all scrapers.
    """

    def __init__(
        self,
        timeout=15,
        pause=0.5,
        user_agent="Mozilla/5.0 (compatible; ScrapingAssignment/1.0)",
    ):
        self.timeout = timeout
        self.pause = pause

        self.logger = logging.getLogger(__name__)

        # Create a reusable HTTP session
        self.session = requests.Session()

        # Set User-Agent
        self.session.headers.update(
            {
                "User-Agent": user_agent
            }
        )

        # Configure retry behavior
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            raise_on_status=False,
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)

        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def fetch(self, url):
        """
        Fetch a webpage using the configured HTTP session.
        """

        try:
            self.logger.info("Requesting URL: %s", url)

            response = self.session.get(
                url,
                timeout=self.timeout,
            )

            response.raise_for_status()

            self.logger.info(
                "Successfully fetched: %s (status=%s)",
                url,
                response.status_code,
            )

            # Respectful pause between requests
            time.sleep(self.pause)

            return response

        except requests.RequestException as error:
            self.logger.error(
                "Request failed for %s: %s",
                url,
                error,
            )

            return None

    def close(self):
        """
        Close the HTTP session.
        """
        self.session.close()