"""
SOCI 40133 HW1 submission for Tim Hannifan. This file performs basic web crawling to extract content from Sputnik news.

Example:
    python crawl.py

Author: Tim Hannifan
"""

import requests
import bs4
import pandas as pd
from scrape import request_content

ARCHIVE_URL = 'https://sputniknews.com/archive/'
BASE_URL = 'https://sputniknews.com'


def process_child(full_url, res):
    """Requests content for a child page and prepares it for a dataframe."""
    html = request_content(full_url)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    res.append({'url': full_url, 'title': soup.title.text}) 


def parse_body_links(html):
    """Iterates through a list of html blocks, identifies child links, and kicks off their requests. Returns a dataframe of urls and page titles."""
    soup = bs4.BeautifulSoup(html, 'html.parser')
    requested = {}
    res = []
    main_content = soup.find_all('li', class_='b-plainlist__item')

    for list_item in main_content:
        links = list_item.find_all('a')
        for link in links:
            url = link.get('href')
            full_url = BASE_URL + url

            if full_url not in requested:
                requested[full_url] = 1
                process_child(full_url, res)

    return pd.DataFrame(res)


def demo_crawler(url):
    """Demo function for crawling sputnik news."""
    df = main(url)
    return df


def main(url=None):
    if url is None:
        url = ARCHIVE_URL
    html = request_content(url)

    return parse_body_links(html)


if __name__ == "__main__":
    main()