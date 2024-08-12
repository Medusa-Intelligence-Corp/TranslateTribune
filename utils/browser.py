import time
import logging

import requests

from urllib import robotparser
from urllib.parse import urlparse

from readabilipy import simple_json_from_html_string

from goose3 import Goose
from goose3.text import StopWordsArabic, StopWordsKorean, StopWordsChinese

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


class UnsupportedModeException(Exception):
    """Exception raised for unsupported modes."""
    def __init__(self, mode, message="Mode not supported"):
        self.mode = mode
        self.message = message
        super().__init__(self.message)


class BadPageException(Exception):
    """Exception raised for bad html codes or bot blocking."""
    def __init__(self, message="url returned bad html code"):
        self.message = message
        super().__init__(self.message)


def setup_driver():
    # Initialize Chrome Options
    chrome_options = Options()
    
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up driver with options
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def fetch_content(url, mode, language):
    headers = {
        "User-Agent": "TranslateTribune/1.0 (https://translatetribune.com)"
    }

    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    robots_url = f"{base_url}/robots.txt"
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)

    try:
        rp.read()
    except requests.exceptions.RequestException:
        logging.info(f"Could not fetch robots.txt from {base_url}")

    if not rp.can_fetch("TranslateTribune", url):
        logging.info(f"Permission issue for {robots_url}, contact them.")

    driver = setup_driver()
    
    response = requests.get(url, headers=headers, timeout=10)
    status_code = response.status_code

    if status_code != 200:
        raise BadPageException(f"Bad status code: {status_code}")

    driver.set_page_load_timeout(90)
    driver.get(url)

    time.sleep(5)
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    if mode=="text":
        text = driver.execute_script("return document.body.innerText")
    elif mode=="source":
        text = driver.page_source
    elif mode=="body":
        text = driver.execute_script("return document.body.outerHTML")
    elif mode=="readability":
        article = simple_json_from_html_string(driver.page_source, use_readability=True)
        text = article["title"] + "\n\n" + article["plain_content"]
    elif mode=="goose":
        if language == "Chinese":
            g = Goose({'stopwords_class': StopWordsChinese})
        elif language == "Arabic":
            g = Goose({'stopwords_class': StopWordsArabic})
        elif language == "Korean":
            g = Goose({'stopwords_class': StopWordsKorean})
        else:
            g = Goose()

        g.http_timeout = 30
        article = g.extract(raw_html=driver.page_source)
        text = article.title + "\n\n" + article.cleaned_text 
    elif mode=="links":
        # check if the url contains codeberg or github
        if "codeberg" in url or "github" in url:
            text = driver.execute_script("""
                function extractTextAndLinks() {
                  // Function to get visible text from an element
                  function getVisibleText(element) {
                    if (element.nodeType === Node.TEXT_NODE) {
                      return element.textContent.trim();
                    }

                    if (element.nodeType !== Node.ELEMENT_NODE) {
                      return '';
                    }

                    const style = window.getComputedStyle(element);
                    if (style.display === 'none' || style.visibility === 'hidden') {
                      return '';
                    }

                    let text = '';
                    for (let child of element.childNodes) {
                      text += getVisibleText(child);
                    }
                    return text;
                  }

                  // Function to convert relative URL to absolute URL
                  function getAbsoluteUrl(relativeUrl) {
                    const a = document.createElement('a');
                    a.href = relativeUrl;
                    return a.href;
                  }

                  const result = [];
                  const containers = document.querySelectorAll('.Box-row, .flex-item');

                  containers.forEach(container => {
                    // Extract visible text from this container
                    const visibleText = getVisibleText(container).replace(/\s+/g, ' ').trim();

                    // Extract hrefs from anchor tags within this container, convert to absolute URLs,
                    // and filter out 'stargazers' and 'forks' links
                    const links = Array.from(container.querySelectorAll('a'))
                      .map(a => getAbsoluteUrl(a.getAttribute('href')))
                      .filter(href => href && !href.includes('stargazers') && !href.includes('forks'));

                    result.push({
                      text: visibleText,
                      links: links
                    });
                  });

                  return result;
                }

                return extractTextAndLinks();
            """)
        else:
            #This selects all 'a' tags, keeps track of their order in the document
            #Then gives the 50 longest links (combined length of url and text)
            #The assumption is that article titles are optimized for SEO
            #and an article name is longer than a command like "Sign Out" or 
            #some other garbage link we don't want to see
            text = driver.execute_script("""
              const links = Array.from(document.querySelectorAll('a'));
              const csvLines = links.map((link, index) => `${index + 1},"${link.textContent.trim()}","${link.href}"`);
              const sortedLines = csvLines.sort((a, b) => b.length - a.length);
              const topTenLines = sortedLines.slice(0, 50);
              const reorderedLines = topTenLines.sort((a, b) => {
                const indexA = parseInt(a.split(',')[0]);
                const indexB = parseInt(b.split(',')[0]);
                return indexA - indexB;
              });
              return reorderedLines.join('\\n');
            """)
    else:
        raise UnsupportedModeException(mode)
    
    driver.quit()

    return text 
