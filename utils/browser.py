import time

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
    driver = setup_driver()
    
    driver.get(url)

    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    if mode=="text":
        text = driver.execute_script("return document.body.innerText")
    elif mode=="source":
        text = driver.page_source
    elif mode=="body":
        text = driver.execute_script("return document.body.outerHTML")
    elif mode=="readability":
        with open("/usr/src/app/node_modules/@mozilla/readability/Readability.js", "r") as file:
            readability_js = file.read()
        driver.execute_script(readability_js)
        text = driver.execute_script("return new Readability(document).parse().content;") 
    elif mode=="goose":
        if language == "Mandarin":
            g = Goose({'stopwords_class': StopWordsChinese})
        elif language == "Arabic":
            g = Goose({'stopwords_class': StopWordsArabic})
        elif language == "Korean":
            g = Goose({'stopwords_class': StopWordsKorean})
        else:
            g = Goose()

        article = g.extract(raw_html=driver.page_source)
        text = article.title + "\n\n" article.cleaned_text 
    elif mode=="links":
        #TODO update this to use new n longest links algo
        text = driver.execute_script(f"""
            return Array.from(document.querySelectorAll('a'))
                .filter(link => link.textContent.trim().length > 30)
                .map(link => `"${{link.textContent.trim()}}","${{link.href}}"`)
                .join('\\n');
        """)
    else:
        raise UnsupportedModeException(mode)
    
    driver.quit()

    return text 
