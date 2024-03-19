import os
import logging

#keep this config here, otherwise logging setup is overwritten
log_path = '/var/log/tt/publisher.log'
os.makedirs(os.path.dirname(log_path), exist_ok=True)
logging.basicConfig(filename=log_path, level=logging.INFO,
                format='%(asctime)s:%(levelname)s:%(message)s')

import time
import re
import json
import traceback
import random

from jinja2 import Template
from bs4 import BeautifulSoup

from browser import fetch_content
from llm import fetch_llm_response, get_model_url
from templater import deploy_website, deploy_games, deploy_books

def publish(sources_filename, template_filename, html_filename, finder_template, summarizer_template):        

    with open(sources_filename, 'r') as file:
        sources_config = json.load(file)

    random.shuffle(sources_config)

    article_dict = {}

    for source_config in sources_config:
        try:
            name = source_config.get("name", "N/A")
            language = source_config.get("language", "N/A")
            flag = source_config.get("flag", "N/A")
            source = source_config.get("source", "N/A")
            source_wiki = source_config.get("source_wiki", "N/A")
            url = source_config.get("url", "N/A")
            
            model = source_config.get("model", "Open Mixtral")
            model_url = source_config.get("model_url", get_model_url(model))
            
            article_title_length = source_config.get("article_title_length",30)
            
            all_links = fetch_content(url,"links",article_title_length) 
            
            logging.info(name)
            logging.info(all_links)

            best_links = fetch_llm_response(
                all_links, finder_template.render(**locals()),
                model, "url")
            
            logging.info(best_links)
            
            if best_links is not None:
                for link in best_links:          
                    article_text = fetch_content(link,"text")
                    logging.info(article_text)                    

                    article_summary = fetch_llm_response(
                            article_text, summarizer_template.render(**locals()),
                            model, "html-article")
                    logging.info(article_summary)
                    
                    soup = BeautifulSoup(article_summary, 'html.parser')
                    article_title = soup.find('div', class_='article-title').text.strip()
                    article = soup.find('article')
                    try:
                        front_page_score = float(article['data-front-page-score'])
                    except (KeyError, ValueError, TypeError):
                        front_page_score = 0.0
                    article_dict[article_title]["html"] = article_summary
                    article_dict[article_title]["score"] = front_page_score
                    
        except Exception as e:
            logging.exception(f"An unexpected error occurred, ignoring: {e}")
            traceback.print_exc()
    
    sorted_articles = sorted(article_dict.items(), key=lambda x: x[1]['score'], reverse=True)
    article_html=""
    for article_title, article_data in sorted_articles:
        article_html += article_data['html']

    completehtml=deploy_website(article_html, template_filename, html_filename)


if __name__ == "__main__":
    deploy_games()
    deploy_books()

    finder_template = Template("""Act as a polyglot international newspaper editor who is an ex-CIA analyst, your goal is to pick the best articles to translate to English. Please review the mess of links and titles provided from {{ source }}, a {{ language }} language newspaper. Ignore any bad links to menus and such, find the links to articles and identify one article that will be interesting to an American reader with global concerns, the article might cover a story of global importance, it might be particularly funny or interesting local story from a far corner of the globe, or it might offer unique insights or perspectives specific to {{ name }}. Choose a story that is current, relevant, and has a significant impact on our readership. The article will be considered for translation into English. If you find there are no suitable articles for translation, please return empty json. I am sure there are some bad links and terrible content, but try and ignore that and find us one good link. We are trusting you to find the 'diamond in the rough'. This is important for our country and for the survival of our newspaper business. Check any links you suggest to make sure they aren't links to files like pdfs (we don't want those). Please respond only in valid json as if you were an API, adhering to the structure provided below: 

    ```
    {
  "best_article":"http://example.com/great-article" 
    }
    ```

  full list of links to review:
""")

    summarizer_template = Template("""Act as a translator and summarizer. Below, I will provide the text of an article in {{ language }}. Please create a summary of the article's content in English, making the summary clear and concise. Avoid using any foreign acronyms that might be confusing to an American reader. Rewrite the title in English so it will be compelling to an American reader.

Additionally, identify and include no more than three {{ language }} vocabulary phrases that would be beneficial for a student learning {{ language }}. Select vocabulary words that are:
- Relevant to the article's content
- Potentially challenging for learners
- Useful in building language skills

When summarizing and translating the article, please assign a "data-front-page-score" attribute to the <div class="article"> element . This score determines the article's placement on the front page.

The "data-front-page-score" attribute should be set to a value between 1 and 5:
- 5: Highest importance, displayed at the top of the front page
- 4: High importance, displayed prominently on the front page
- 3: Moderate importance, displayed in the middle section of the front page
- 2: Low importance, displayed in the lower section of the front page
- 1: Lowest importance, may be displayed at the bottom of the front page or omitted

Format the response exclusively in valid HTML, adhering to this structure:

```
<div class="article" data-front-page-score="0">
    <div class="article-title" onclick="toggleArticleDetails(this)">
        <!-- DO NOT CHANGE THE FLAG BELOW, IT MUST DISPLAY THE FLAG OF {{ name|upper }} -->
        <span class="flag-icon" role="img" aria-label="Flag of {{ name }}">{{ flag }}</span>
        Title in English goes here.
    </div>
    <p class="article-content hidden">English summary of the article goes here, following The Economist's style guide but using American spelling. </p>
    <ul class="vocabulary hidden">
      <li>{{ language }} word 1 - English translation goes here</li>
      <li>{{ language }} word 2 - English translation goes here</li>
      <li>{{ language }} word 3 - English translation goes here</li>
    </ul>
    <div class="article-credit hidden">
      <a href="{{ model_url }}">Summary by {{ model }}</a>
      <a href='{{ link }}'>Full article in {{language}}</a>
      <a href='{{ source_wiki }}'>{{ source }} (Wikipedia)</a>
    </div>
</div>
```

If the provided article text appears to be gathered in error or does not have an article to summarize, respond with only the text ```<h1>MISSING ARTICLE</h1>```.

Do not include any additional text or formatting outside of the specified HTML tags.

article text:""")
                        
    debug = os.environ.get('DEBUG', False)
    if debug:
        publish('config/sources_debug.json','template.html','index.html',finder_template, summarizer_template)
    else:
        publish('config/sources.json','template.html','index.html',finder_template, summarizer_template)

    finder_template_business = Template("""Act as a polyglot international finance and technology newspaper editor who is a former Goldman Sachs International Equity Analyst and Google Engineer, your goal is to pick the best articles to translate to English. Please review the mess of links and titles provided from {{ source }}, a {{ language }} language newspaper. Ignore any bad links to menus and such, find the links to articles and identify one article that will be interesting to an American reader with global concerns, the article might cover a technology or finance story of global importance or it might offer unique insights or perspectives specific to the technology or financial news of {{ name }}. Choose a story that is current, relevant, and has a significant impact on our readership. The article will be considered for translation into English. If you find there are no suitable articles for translation, please return empty json. I am sure there are some bad links and terrible content, but try and ignore that and find us one good link. We are trusting you to find the 'diamond in the rough'. This is important for each issue to translate good stories to keep our readers engaged, so try your best. Check any links you suggest to make sure they aren't links to files like pdfs (we don't want those). Please respond only in valid json as if you were an API, adhering to the structure provided below: 

    ```
    {
  "best_article":"http://example.com/great-article" 
    }
    ```

  full list of links to review:
""")
    if not debug:
        publish('config/sources_technology_finance.json','template.html','finance-and-technology.html',finder_template_business, summarizer_template)
