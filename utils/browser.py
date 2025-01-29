import time
import logging

from tempfile import mkdtemp

from readabilipy import simple_json_from_html_string

from goose3 import Goose
from goose3.text import StopWordsArabic, StopWordsKorean, StopWordsChinese

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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
    chrome_options = Options()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(f'--user-data-dir={mkdtemp()}')
    chrome_options.set_capability("pageLoadStrategy", "normal")
    chrome_options.set_capability("timeouts", {
        "implicit": 60000,
        "pageLoad": 90000,
        "script": 60000
    })

    driver = webdriver.Chrome(
        options=chrome_options
    )

    return driver


def fetch_content(url, mode, language):
    driver = None
    try:
        driver = setup_driver()

        time.sleep(5)
        driver.get(url)

        WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

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
            if "codeberg.org" in url:
                with open('utils/codeberg_extractor.js', 'r') as file:
                    js_script = file.read()
                text = driver.execute_script(js_script).replace('\\n', '\n')
            elif "github.com" in url:
                with open('utils/github_extractor.js', 'r') as file:
                    js_script = file.read()
                text = driver.execute_script(js_script).replace('\\n', '\n')
            else:
                with open('utils/link_extractor.js', 'r') as file:
                    js_script = file.read()
                text = driver.execute_script(js_script)
        else:
            raise UnsupportedModeException(mode)
    except Exception as e:
        logging.error(f"Error during content fetch: {str(e)}")
        raise
    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                logging.error(f"Error closing driver: {str(e)}")

    return text 
