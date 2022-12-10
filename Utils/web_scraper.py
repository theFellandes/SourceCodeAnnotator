from dataclasses import dataclass

import requests
import urllib
from requests_html import HTMLSession
from googlesearch import search


@dataclass
class WebScraper:
    query: str
    google_link: str = "https://www.google.com/search?q="

    @staticmethod
    def get_source(url):
        """Return the source code for the provided URL.

        Args:
            url (string): URL of the page to scrape.

        Returns:
            response (object): HTTP response object from requests_html.
        """

        try:
            session = HTMLSession()
            response = session.get(url)
            return response

        except requests.exceptions.RequestException as e:
            print(e)

    def get_results(self):
        """ Returns response generated from google """
        query = urllib.parse.quote_plus(self.query)
        response = self.get_source(self.google_link + query)
        return response

    @staticmethod
    def parse_results(response):
        """ Returns list of items retrieved from css_identifiers """
        css_identifier_result = ".tF2Cxc"
        css_identifier_title = "h3"
        css_identifier_link = ".yuRUbf a"
        css_identifier_text = ".VwiC3b"

        results = response.html.find(css_identifier_result)

        output = []

        for result in results:
            try:
                item = {
                    'title': result.find(css_identifier_title, first=True).text,
                    'link': result.find(css_identifier_link, first=True).attrs['href'],
                    'text': result.find(css_identifier_text, first=True).text
                }
            except AttributeError:
                continue

            output.append(item)

        return output

    def search_google(self):
        """ Returns the contents and the links of the search result """
        response = self.get_results()
        return self.parse_results(response)

    def search_google_with_yield(self, num_results: int = 10):
        """ Returns the links with generator """
        yield search(self.query, lang="en", num_results=num_results)

    def scrape_google(self):
        """ Returns the links of the search result """
        response = self.get_results()

        links = list(response.html.absolute_links)
        google_domains = ('https://www.google.',
                          'https://google.',
                          'https://webcache.googleusercontent.',
                          'http://webcache.googleusercontent.',
                          'https://policies.google.',
                          'https://support.google.',
                          'https://maps.google.')

        for url in links[:]:
            if url.startswith(google_domains):
                links.remove(url)

        return links


if __name__ == '__main__':
    web_scraper = WebScraper('System.out.println()')
    print(web_scraper.search_google())
    print("")
    print("")
    print("")
    print(web_scraper.scrape_google())
