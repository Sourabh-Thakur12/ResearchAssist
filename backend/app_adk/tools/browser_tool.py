import requests
from bs4 import BeautifulSoup
from readability import Document

class BrowserTool:
    """
    Lightweight browser tool for retrieving and cleaning webpage content.
    Ideal for research use cases (blogs, articles, documentation).
    """

    def __init__(self, timeout=10):
        self.timeout = timeout
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        }

    def scrape(self, url: str) -> str:
        """Fetch the page and extract clean readable text."""
        try:
            # 1. download raw page
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()

            html = response.text

            # 2. Use readability to isolate main article content
            readable_doc = Document(html)
            summary_html = readable_doc.summary()

            # 3. Parse into clean text
            soup = BeautifulSoup(summary_html, "lxml")
            text = soup.get_text(separator="\n", strip=True)

            return text

        except Exception as e:
            return f"[BrowserTool Error] Failed to scrape {url}: {e}"
