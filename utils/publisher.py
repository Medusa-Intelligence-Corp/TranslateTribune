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

def publish(sources_filename, template_filename, html_filename, finder_template, persona, summarizer_template):        

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
                    article = soup.find('div', class_='article')
                    try:
                        front_page_score = float(article['data-front-page-score'])
                    except (KeyError, ValueError, TypeError):
                        front_page_score = 0.0
                    article_dict[article_title] = {}
                    article_dict[article_title]["html"] = article_summary
                    article_dict[article_title]["score"] = front_page_score
                    
        except Exception as e:
            logging.exception(f"An unexpected error occurred, ignoring: {e}")
            traceback.print_exc()
    
    sorted_articles = sorted(article_dict.items(), key=lambda x: x[1]['score'], reverse=True)
    article_html=""
    for article_title, article_data in sorted_articles:
        article_html += article_data['html']

    complete_html = deploy_website(article_html, template_filename, html_filename)
    logging.info(complete_html)


def load_template(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return Template(file.read())


if __name__ == "__main__":
    deploy_games()
    deploy_books()

    finder_template = load_template('config/finder.txt')
    summarizer_template = load_template('config/summarizer.txt')

    # Create the homepage
    persona = "an international newspaper editor who is an ex-CIA analyst"    
    
    debug = os.environ.get('DEBUG', False)
    config_file = 'config/sources_debug.json' if debug else 'config/sources.json'
    
    publish(config_file, 'template.html', 'index.html', finder_template, persona, summarizer_template)

    # Create the finance and technology page
    if not debug:
        tech_persona= "an international finance and technology newspaper editor who is a former Goldman Sachs International Equity Analyst and Google Engineer"
        publish('config/sources_technology_finance.json','template.html','finance-and-technology.html',finder_template, tech_persona, summarizer_template)
