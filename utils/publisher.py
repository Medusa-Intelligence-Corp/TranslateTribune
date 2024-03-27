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
import html

from cachetools import LRUCache, TTLCache

article_cache = LRUCache(maxsize=100)
link_cache = TTLCache(maxsize=100, ttl=3600)

from jinja2 import Template
from bs4 import BeautifulSoup

from browser import fetch_content
from llm import fetch_llm_response
from templater import deploy_website, deploy_games

def publish(sources_config, lang_config, finder_template, \
        summarizer_template, html_filename, persona_type="persona"):        

    random.shuffle(sources_config)

    article_dict = {}

    for source_config in sources_config:
        try:
            #as a rule, we don't publish same-language summaries
            if source_config["source_language"] == lang_config["publishing_language"]:
                continue

            try:
                all_links = link_cache[source_config["source_url"]]
            except KeyError:
                all_links = fetch_content(source_config["source_url"],\
                        "links",\
                        source_config["source_language"]) 
                link_cache[source_config["source_url"]] = all_links

            logging.info(source_config["source"])

            best_links = fetch_llm_response(
                all_links,\
                finder_template.render(**locals()),\
                source_config["finder_model"],\
                "url")
            
            logging.info(best_links)
            
            #we are only expecting one link, slice the list to just select the first item
            link = best_links[0]
            #sometimes the llm shares the link like "here's the link https://example.com/article."
            #periods are valid at the end of links, but this almost never happens in practice
            #so we remove the period here
            if link.endswith('.'):
                link = link[:-1]

            #When iterating over many languages, the link selector often picks the same article
            #regardless of the persona given, so to not get our IP address blocked, it's nice of 
            #us to do some caching
            try:
                article_text = article_cache[link]
            except KeyError:
                article_text = fetch_content(link,\
                        source_config["source_parser"],\
                        lang_config["publishing_language"])
                article_cache[link] = article_text

            article_summary = fetch_llm_response(
                    article_text,\
                    summarizer_template.render(**locals()),\
                    source_config["summarizer_model"],\
                    "html-article")
            
            # Save the title
            soup = BeautifulSoup(article_summary, 'html.parser')
            title_div = soup.find('div', class_='article-title')
            article_title=title_div.text.strip()
           
            if title_div:
                flag_span = soup.new_tag('span',\
                        attrs={'role': 'img', 'aria-label': f'Flag of {source_config["source_country"]}'})
                flag_span.string = html.unescape(source_config["source_flag"])
                title_div.insert(0, flag_span)
                title_div.insert(1, ' ')

            content_div = soup.find('div', class_='article-content')

            if content_div:
                link = soup.new_tag('a', href=link)
                link.string = source_config["source"]
                content_div.append(' ')
                content_div.append(link)

            title_div = soup.find('div', class_='article-title')

            if title_div:
                title_div['onclick'] = 'toggleArticleDetails(this)'
                                
            article_summary = str(soup)

            # Get the front page score
            article = soup.find('div', class_='article')
            front_page_score = float(article['data-front-page-score'])
            
            article_dict[article_title] = {}
            article_dict[article_title]["html"] = article_summary
            article_dict[article_title]["score"] = front_page_score
            
            logging.info(article_summary)
        except Exception as e:
            logging.exception(f"An unexpected error occurred, ignoring: {e}")
            traceback.print_exc()
    
    sorted_articles = sorted(article_dict.items(), key=lambda x: x[1]['score'], reverse=True)
    article_html=""
    for article_title, article_data in sorted_articles:
        if article_data['score'] > 2:
            article_html += article_data['html']

    complete_html = deploy_website(article_html,html_filename,lang_config)
    logging.info(complete_html)


def load_template(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return Template(file.read())


def get_language_config(language):
    with open('config/languages.json', 'r') as file:
        lang_configs = json.load(file)
    
    for item in lang_configs:
        if item.get("publishing_language") == language:
            return item
    return None


def get_sources_config(filename):
    with open(filename, 'r') as file:
        sources_config = json.load(file)
    return sources_config

def deploy_language(publishing_language):
    lang_config = get_language_config(publishing_language)
    
    finder_template = load_template('config/finder.txt')
    summarizer_template = load_template('config/summarizer.txt')
    
    debug = os.environ.get('DEBUG', False)
    sources_filename = 'config/sources_debug.json' if debug else 'config/sources.json'
    
    publish(get_sources_config(sources_filename),\
            lang_config,\
            finder_template,\
            summarizer_template,\
            f'{lang_config["publishing_language_short"]}.html')

    # Create the finance and technology page
    if not debug:
        publish(get_sources_config('config/sources_finance_technology.json'),\
                lang_config,\
                finder_template,\
                summarizer_template,\
                f'{lang_config["publishing_language_short"]}-ft.html',\
                "finance_technology_persona")

if __name__ == "__main__":
    debug = os.environ.get('DEBUG', False)
    
    if debug:
        deploy_language("English")
        deploy_language("Spanish")
    else:
        with open('config/languages.json', 'r') as file:
            lang_configs = json.load(file)
        
        for lang_config in lang_configs:
            deploy_language(lang_config["publishing_language"])
