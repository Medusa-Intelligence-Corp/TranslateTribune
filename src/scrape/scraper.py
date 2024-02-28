from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def setup_driver():
    # Path to the bypass paywalls extension
    extension_path = '/usr/src/app/bypass-paywalls-chrome-clean-master'

    # Initialize Chrome Options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'--load-extension={extension_path}')

    # Set up driver with options
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def scrape_nytimes():
    driver = setup_driver()
    driver.get("https://www.nytimes.com")

    # Implement your scraping logic here
    # For example, to print the page title:
    print(driver.title)

    # Clean up
    driver.quit()

if __name__ == "__main__":
    scrape_nytimes()

