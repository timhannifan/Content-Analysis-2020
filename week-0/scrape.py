"""
SOCI 40133 HW1 submission for Tim Hannifan. This file demonstrates scraping web pages with beautifulsoup.

Example:
    python scrape.py

Author: Tim Hannifan
"""
import requests
import bs4
import re
import pandas as pd

SCRAPE_BASE_URL = 'https://www.rt.com/news/'
DEMO_SCRAPE_URL = 'https://www.rt.com/news/485890-who-defunding-global-outcry/'
DEMO_OUT_FNAME = 'demo_html.html'


def write_text_to_file(filename, content):
    """Writes text content to  a file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print('Error writing to file: ', e)


def request_content(url):
    """Creates an HTTP request and returns the text content if possible."""
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.text
    except requests.HTTPError as e:
        print(e)

def scrape_html(html):
    """Scrapes body content from a rt.com news article.."""
    soup = bs4.BeautifulSoup(html, 'html.parser')
    res = []

    main_content = soup.find('div', class_='article__text')
    if main_content is not None:

        for p in main_content('p'):
            #Embedded tweets contain the 'dir' attribute and are removed.
            tweet_sig = p.attrs.get('dir')
            if tweet_sig is not None and 'ltr' in tweet_sig:
                continue
            else:
                res.append(p.text)

    return res

def clean_text(paragraphs, patterns):
    """Iterates through a list of paragraphs and does regex substitutions."""
    res = []
    for paragraph in paragraphs:
        for _p in patterns:
            pattern, sub = _p
            p = re.compile(pattern)
            paragraph = p.sub(sub, paragraph)
        if len(paragraph) > 0:
            res.append(paragraph)
    return res


def demo_rt_paragraphs(url):
    """Demo function for scraping paragraphs to a dataframe."""
    df = main(url)
    return df

def main(url=None):
    """Main function for running the scraping process."""
    regex_substitutions = [
        (r'[“”]', ''),       # remove quotes
        (r'[,-]', ' '),       # remove commas and hyphens
        (r'\d', ' '),       # remove digits
        (r'\s{2,}', ' '),   # clean up two or more spaces
        (r'[\s]$', '')      # remove trailing spaces
    ]

    if url is None:
        url = DEMO_SCRAPE_URL
    html = request_content(url)
    write_text_to_file(DEMO_OUT_FNAME, html)

    paragraphs = scrape_html(html)
    clean_paragraphs = clean_text(paragraphs, regex_substitutions)
    paragraph_df = pd.DataFrame({'paragraphs' : clean_paragraphs})
    return paragraph_df

if __name__ == "__main__":
    main()
