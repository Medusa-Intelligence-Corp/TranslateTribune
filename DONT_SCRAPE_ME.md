# How TranslateTribune Uses Web Scraping Technology

TranslateTribune is a news aggregator that translates and summarizes web content, which we believe falls under fair use. We strive to comply with the law and respect publishers' requests not to scrape their content. Our summaries are similar to social media posts about articles but in different languages. We always link to our sources and never post full articles.

Our scraper follows robots.txt preferences, avoids using hacks to bypass paywalls (e.g., we don't use [bypass-paywalls-chrome-clean](https://gitlab.com/magnolia1234/bypass-paywalls-chrome-clean)), identifies itself as "TranslateTribune", and uses caching to minimize bandwidth usage. You will typically see only a handful of visits from us per day.

## TranslateTribune Scraper Workflow

The [TranslateTribune scraper code (browser.py)](./utils/browser.py) works as follows:

1. Sets custom User-Agent header to identify as "TranslateTribune/1.0"
2. Parses target URL to extract base domain
3. Fetches robots.txt from domain and checks permission to access target URL
4. Uses Selenium with headless Chrome to load full page
5. Fetches page content and checks for 200 OK status code, raising an exception otherwise
6. Extracts page content for further processing
7. Caches scraped result temporarily (few hours) and deletes it, never saving the source article permanently

# Protecting Your News Site from Web Scraping

To make it harder for scrapers to bypass your paywall and access articles, consider these best practices:

## 1. Implement a Sophisticated Paywall
- Require user login and authentication for full articles
- Detect and block suspicious activity (e.g., abnormally fast page views from an IP)
- Serve article text and media via JavaScript to prevent access by disabling JS
    - The paywalls of [nytimes.com](https://www.nytimes.com) never work if you are browsing without JavaScript, making them totally ineffective against web scraping
    - The [wsj.com](https://www.wsj.com) has a very effective paywall that is difficult to circumvent
    - No matter what you do, if you are popular enough your paywall will probably be circumvented by a project like [bypass-paywalls-chrome-clean](https://gitlab.com/magnolia1234/bypass-paywalls-chrome-clean), but it's still worth trying to do it 'right' to make life harder for cheap bots (written by bad developers) to get your data if you don't want them to.

## 2. Configure a Complete robots.txt
- Clearly disallow scraping of protected content in robots.txt
- List all URL patterns to protect (e.g., /articles/*, /videos/*)
- Avoid unnecessary legal terms, as robots.txt is not legally binding
- Good example: [WSJ robots.txt](https://www.wsj.com/robots.txt) is complete without extraneous legalese
- Bad example: [NYT robots.txt](https://www.nytimes.com/robots.txt) includes legalese which does not provide additional protection
- Permissive Example: [USA Today robots.txt](https://www.usatoday.com/robots.txt) allows many scrapers
- Allow Everything: [TranslateTribune robots.txt](http://translatetribune.com/robots.txt) we don't care, scrape and index away

## 3. Monitor and Block Suspicious Traffic
- Log and monitor page views to detect anomalous scraping behavior
- Block IPs and user agents with suspicious access patterns
- Limit the rate at which a client can access pages

## 4. Send Letters When Needed
- Send cease and desist notices to detected scrapers
- You can ask us to stop by emailing [editor@translatetribune.com](mailto:editor@translatetribune.com)
- Have a clear Terms of Service prohibiting scraping and unauthorized access
- Ensure the scraper is located where legal action is feasible; otherwise, focus on improving your paywall or blocking traffic
