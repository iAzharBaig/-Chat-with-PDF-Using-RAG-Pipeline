import requests
from bs4 import BeautifulSoup
from typing import Optional
import logging
from urllib.parse import urlparse

class WebCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def validate_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def crawl_and_scrape(self, url: str) -> Optional[str]:
        if not self.validate_url(url):
            raise ValueError(f"Invalid URL: {url}")

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for element in soup(['script', 'style', 'meta', 'header', 'footer']):
                element.decompose()
                
            text = ' '.join(soup.stripped_strings)
            return text if text.strip() else None
            
        except requests.RequestException as e:
            logging.error(f"Error crawling {url}: {str(e)}")
            return None

# Initialize global instance
crawler = WebCrawler()

def crawl_and_scrape(url: str) -> Optional[str]:
    return crawler.crawl_and_scrape(url)