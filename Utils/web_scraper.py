from dataclasses import dataclass

import re
import requests
import urllib
from requests_html import HTMLSession
from googlesearch import search


@dataclass
class WebScraper:
    query: str
    doc_site: str = ''
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
        response = self.get_source(self.google_link + query + self.doc_site)
        return response

    @staticmethod
    def parse_results(response):
        """ Returns list of items retrieved from css_identifiers """
        css_identifier_result = ".tF2Cxc"
        css_identifier_link = ".yuRUbf a"
        css_identifier_text = ".VwiC3b"

        results = response.html.find(css_identifier_result)

        output = []

        for result in results:
            try:
                item = {
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


    @staticmethod
    def traverse_result(search_result):
        for result in search_result:
            return re.findall('The [a-zA-Z]+\(\)', result.strip())


if __name__ == '__main__':
    web_scraper = WebScraper('println()', 'site:docs.oracle.com')
    print(web_scraper.search_google()[0])
    web_scraper.query = 'indexOf()'
    print(web_scraper.search_google()[0])
    # web_scraper.query = 'toCharArray()'
    # print(web_scraper.search_google()[0])
    # web_scraper.query = 'replace()'
    # print(web_scraper.search_google()[0])
    # web_scraper.query = 'substring()'
    # print(web_scraper.search_google()[0])
    # web_scraper.query = 'getUserId()'
    # print(web_scraper.search_google()[0])
    # print(" ")
    # print(" ")
    # print(" ")
    # print(" ")
    # print(" ")
    print("Python")
    web_scraper_python = WebScraper('print()',
                                    'site:docs.python.org/3/library/functions.html')
    print(web_scraper_python.search_google()[0].get('text').partition("."))
    web_scraper_python.query = 'input()'
    a = web_scraper_python.search_google()[0].get('text').partition(".")
    print(web_scraper_python.search_google()[0].get('text').partition("."))
    print(web_scraper_python.traverse_result(a))
    web_scraper_python.query = 'len()'
    a = web_scraper_python.search_google()[0].get('text').partition(".")
    print(web_scraper_python.search_google()[0].get('text').partition("."))
    print(web_scraper_python.traverse_result(a))
    web_scraper_python.query = 'replace()'
    a = web_scraper_python.search_google()[0].get('text').partition(".")
    print(web_scraper_python.search_google()[0].get('text').partition("."))
    print(web_scraper_python.traverse_result(a))
    web_scraper_python.query = 'split()'
    a = web_scraper_python.search_google()[0].get('text').partition(".")
    print(web_scraper_python.search_google()[0].get('text').partition("."))
    print(web_scraper_python.traverse_result(a))

