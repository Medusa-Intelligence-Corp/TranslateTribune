import re
import json
import traceback
import random

from jinja2 import Template
from bs4 import BeautifulSoup

from browser import fetch_content
from llm import fetch_llm_response
from templater import deploy_website

def publish(sources_filename, template_filename, html_filename, finder_template, summarizer_template, prioritizer_template):    
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
            model = source_config.get("model", "Claude 3")
            model_url = source_config.get("model_url", "https://www.anthropic.com/claude")
            chunk_approx_tokens = source_config.get("tokens", 150000)
            avg_token_length = source_config.get("token_length", 3)
            article_title_length = source_config.get("article_title_length",30)
            
            all_links = fetch_content(url,"links",article_title_length) 
            
            best_links = fetch_llm_response(
                all_links, finder_template.render(**locals()),
                model, chunk_approx_tokens, avg_token_length, "url")
            print(best_links)
            
            if best_links is not None:
                for link in best_links:          
                    article_text = fetch_content(link,"text") 
                    article_summary = fetch_llm_response(
                            article_text, summarizer_template.render(**locals()),
                            model, chunk_approx_tokens, avg_token_length, "html")
                    print(article_summary)
                    soup = BeautifulSoup(article_summary, 'html.parser')
                    article_title = soup.find('div', class_='article-title').text.strip()
                    article_dict[article_title] = article_summary
                    
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            traceback.print_exc()
            print("continuing anyway...")
    
    title_text=json.dumps(list(article_dict.keys()))
    title_dict = fetch_llm_response(
                    title_text, prioritizer_template.render(**locals()),
                    'Claude 3', 100000, 3, "json")

    article_html=""
    for item in title_dict.get('articles',[]):
        try:
            print(item)
            article_html+=article_dict.pop(item.get('title','N/A'))
        except KeyError:
            print("skipping messed up title from LLM")
    for key,value in article_dict.items():
        article_html+=value
    completehtml=deploy_website(article_html, template_filename, html_filename)


if __name__ == "__main__":
    finder_template = Template("""Act as a polyglot international newspaper editor who is an ex-CIA analyst, your goal is to pick the best articles to translate to English. Please review the article links and titles provided from {{ source }}, a {{ language }} language newspaper. Identify one article that offers unique insights or perspectives specific to {{ name }}. The article will be considered for translation into English. If you find there are no suitable articles for translation, please return the link to the most interesting article in the list. I am sure there are some bad links and terrible content, but try and ignore that and find us one good link. We are trusting you to find the 'diamond in the rough'. This is important for our country and for the survival of our newspaper business. Check any links you suggest to make sure they aren't links to files like pdfs (we don't want those). Please respond only in valid json as if you were an API.

Article list:
""")

    summarizer_template = Template("""Act as a translator and summarizer. Below, I will provide the text of an article in {{ language }}. Please, create a summary of the article's content in English, make the summary clear and consise, avoid using any foreign acronyms that might be confusing to an American reader. Additionally, identify and include a few key $language vocabulary phrases that would be beneficial for a student learning {{ language }}. The response should be formatted exclusively in valid HTML, adhering to the structure provided below:

                    return format:             
                    ```
                    <div class="article">
                        <div class="article-title" onclick="toggleArticleDetails(this)">
                            <span class="flag-icon" role="img" aria-label="Flag of {{ name }}">{{ flag }}</span>TITLE IN ENGLISH
                        </div>
                        <p class="article-content hidden">SUMMARY IN ENGLISH</p>
                        <ul class="vocabulary hidden">
                          <li>${{ language|upper }}-ENGLISH VOCABULARY WORD</li>
                          <li>${{ language|upper }}-ENGLISH VOCABULARY WORD</li>                          
                          <li>${{ language|upper }}-ENGLISH VOCABULARY WORD</li>
                          <li>${{ language|upper }}-ENGLISH VOCABULARY WORD</li>
                        </ul>
                        <div class="article-credit hidden">
                          <a href="{{ model_url }}">Summary by {{ model }}</a>
                          <a href='{{ link }}'>Full article in {{language}}</a>
                          <a href='{{ source_wiki }}'>$source (Wikipedia)</a>
                        </div>
                    </div>
                    ```

                    Please ensure that the summary provides a clear, concise overview of the article's main points, and select vocabulary words that are relevant to the article's content, potentially challenging for learners, and useful in building their language skills. Follow The Economist's style guide for the summary if you can, but use American spelling. The HTML output should strictly follow the provided structure, with no additional text or formatting outside of the specified HTML tags.

                        article text:
                        """)
                        
    prioritizer_template = Template("""Act as a newspaper editor working on which titles should appear highest on the front page, please re-order and prioritize the titles below by the order they should appear on the front page. The current order is random and you need to decide which titles will be most appealing and drive the most traffic to the news site, and put those articles on the top. Please do not change the article titles and return only valid json as if you were an API, adhering to the structure provided below: 

    ```
    {
  "articles": [
    {
      "title": "ARTICLE TITLE",
      "position": 1
    },
    {
      "title": "ARTICLE TITLE",
      "position": 2
    },
    ...more articles below
  ]
}
```

    current article titles (in random order):
    """)
    
    publish('sources.json','template.html','index.html',finder_template, summarizer_template, prioritizer_template)

    finder_template_business = Template("""Act as a polyglot international finance and technology newspaper editor who is a former Goldman Sachs International Equity Analyst and Google Engineer, your goal is to pick the best articles to translate to English. Please review the article links and titles provided from {{ source }}, a {{ language }} language newspaper. Identify one article that offers unique insights, technology news, economic or business perspectives specific to {{ name }}. The article will be considered for translation into English. If you find there are no suitable articles for translation, please return the link to the most interesting article in the list, something that an American audience might find humourous or might help win a trivia contest one day. I am sure there are some bad links and terrible content, but try and ignore that and find us one good link. We are trusting you to find the 'diamond in the rough'. This is important for each issue to translate good stories to keep our readers engaged, so try your best. Check any links you suggest to make sure they aren't links to files like pdfs (we don't want those). Please respond only in valid json as if you were an API.

Article list:
""")
    publish('sources_technology_finance.json','template.html','technology-and-finance.html',finder_template_business, summarizer_template, prioritizer_template)
