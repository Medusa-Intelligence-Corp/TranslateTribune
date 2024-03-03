import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

class UnsupportedModelException(Exception):
    """Exception raised for unsupported models."""
    def __init__(self, model, message="Model not supported"):
        self.model = model
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

def send_to_anthropic(text_chunk, instructions):
    anthropic = Anthropic()

    completion = anthropic.completions.create(
        model="claude-2.1",
        max_tokens_to_sample=200000,
        prompt=f"{HUMAN_PROMPT} {instructions}:\n{text_chunk}{AI_PROMPT}",
    )

    return completion.completion

def get_best_article(url, instructions, model):
    # TODO
    article_url = "https://localhost"
    return article_url

def get_article_summary(url, instructions, model):
    driver = setup_driver()
    
    driver.get(url)

    # Wait for the page to load
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Use JavaScript to get all text content from the body element
    # This includes text within script tags and dynamically loaded content
    # NOTE: if you need to bypass a login or something, look for tampermonkey scripts
    text = driver.execute_script("return document.body.innerText")
    print(text)


    # TODO check for token size and chunk if needed
    if model=="Claude 2":
        summary = send_to_anthropic(text, instructions)
    else:
        raise UnsupportedModelException(model)

    print(summary)

    # Clean up
    driver.quit()

if __name__ == "__main__":
    #TODO get json from file and iterate through sources
    #TODO randomize the order that you process
    scrape("https://avis-vin.lefigaro.fr/domaines-et-vignerons/o157408-biodynamie-polyculture-elevage-decouverte-d-un-domaine-pas-comme-les-autres-a-chinon")

    #TODO use an html template here and output it
    print("Done")

