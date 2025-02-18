import os
import logging

#keep this config here, otherwise logging setup is overwritten
log_path = '/var/log/tt/publisher.log'
os.makedirs(os.path.dirname(log_path), exist_ok=True)
logging.basicConfig(filename=log_path, level=logging.INFO,
                format='%(asctime)s:%(levelname)s:%(message)s')

import time
import datetime
import uuid
import re
import json
import random
import html
import shutil

from cachetools import LRUCache, TTLCache

article_cache = LRUCache(maxsize=100)
link_cache = TTLCache(maxsize=100, ttl=3600)

import bleach
from jinja2 import Template
from bs4 import BeautifulSoup
from langdetect import detect
from smartenough import get_smart_answer
from func_timeout import func_timeout, FunctionTimedOut

from browser import fetch_content
from templater import deploy_website


def add_required_html(article_summary, article_url, source_config, lang_config, finder_model, summarizer_model):
        # Add HTML comment with model information for debugging
        article_summary = f"""<!-- Finder Model:     {finder_model} -->\n
                              <!-- Summarizer Model: {summarizer_model} -->  
                              {article_summary}"""

        # Save the title
        soup = BeautifulSoup(article_summary, 'html.parser')
        article_div = soup.find('div', class_='article')
        title_div = soup.find('div', class_='article-title')
        article_title=title_div.text.strip()
    

        if article_div:
            if lang_config.get("is_rtl", False):
                article_div["dir"] = "rtl"

            article_header_div = soup.new_tag('div', attrs={"class": "article-header"})
            flag_img = soup.new_tag('img', src=source_config["source_flag"], attrs={"class": 'source-flag'})
            flag_emoji = soup.new_tag('span', attrs={"class": "hidden"})
            flag_emoji.string = html.unescape(source_config["source_flag_emoji"])

            source_country_span = soup.new_tag('span', attrs={"class": "source-country"})
            source_country_span.string = html.unescape(source_config["source_country"])

            article_header_div.append(flag_img)
            article_header_div.append(flag_emoji)
            article_header_div.append(source_country_span)
            article_div.insert(0, article_header_div)
            article_div['onclick'] = 'toggleArticleDetails(this)'
       
        if title_div:
            article_id = str(uuid.uuid4())
            title_div['id'] = article_id

        content_div = soup.find('div', class_='article-content')


        if content_div:
            link = soup.new_tag('a', href=article_url)
            link['onclick'] = 'event.stopPropagation();'
            wrapper_div = soup.new_tag('div')
            source_name_span = soup.new_tag('span')
            source_name_span.string = "Go to " + source_config["source"]
            svg_html = '''
                        <svg
                            width="32"
                            height="32"
                            viewBox="0 0 32 32"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                            >
                            <path
                                d="M31.7071 16.7071C32.0976 16.3166 32.0976 15.6834 31.7071 15.2929L25.3431 8.92893C24.9526 8.53841 24.3195 8.53841 23.9289 8.92893C23.5384 9.31946 23.5384 9.95262 23.9289 10.3431L29.5858 16L23.9289 21.6569C23.5384 22.0474 23.5384 22.6805 23.9289 23.0711C24.3195 23.4616 24.9526 23.4616 25.3431 23.0711L31.7071 16.7071ZM0 17H31V15H0V17Z"
                                fill="black"
                            />
                        </svg>
                    '''
            bg_div=soup.new_tag('div', attrs={"class": "rotated-background-btn"})        
            wrapper_div.append(source_name_span)
            wrapper_div.append(BeautifulSoup(svg_html, 'html.parser'))
            wrapper_div.append(bg_div)
            
            link.append(wrapper_div)

            content_div.append(' ')
            content_div.append(link)             
                            
        article_summary = str(soup)

        # Get the front page score
        article = soup.find('div', class_='article')
        front_page_score = float(article['data-front-page-score'])

        return article_title, article_summary, front_page_score, article_id 
 

def simplify_html(html):
    allowed_tags = ['div', 'span', 'p', 'a']
    allowed_attributes = {'a': ['href']}

    cleaned_html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attributes, strip=True)

    return cleaned_html


def validate_article_html(html, language_code, min_article_score):
    max_size = 10000
    if len(html) > max_size:
        return False

    soup = BeautifulSoup(html, 'html.parser')

    if soup.find('script'):
        return False

    allowed_tags = ['div', 'p', 'ul', 'ol', 'li']
    allowed_attributes = ['class', 'id', 'alt', 'data-front-page-score']

    # Sanitize HTML tags and attributes
    for tag in soup.find_all():
        if tag.name not in allowed_tags:
            tag.decompose()
        for attr in list(tag.attrs.keys()):
            if attr not in allowed_attributes:
                del tag[attr]

    article_content = None
    article_div = soup.find('div', class_='article',\
            attrs=lambda attrs: 'data-front-page-score'\
            in attrs and min_article_score <= int(attrs['data-front-page-score']) <= 5)
    if article_div:
        article_title_div = article_div.find('div', class_='article-title')
        if article_title_div:
            article_content = article_div.find('div', class_='article-content hidden')

    if article_content is None:
        return False

    content_text = article_content.text.strip()
    llm_output_language = detect(content_text)
    logging.info(f"detected output language {llm_output_language}")
    if language_code not in llm_output_language:
        logging.info(f"Wrong Language from LLM. \
                Expected {language_code}\
                got {llm_output_language}")
        return False

    return True


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
    
    
def get_available_ads(lang_code):
    with open('config/ads.json', 'r') as file:
        ad_configs = json.load(file)

    available_ads = []

    for item in ad_configs:
        if lang_code in item:
            available_ads.append(item)
            
    return available_ads


def get_finder_models(lang1):
    models1 = set(get_language_config(lang1).get("supported_models",[]))  # Get models for lang1, default to empty if not found
    return list(models1)


def get_summarizer_models(lang1, lang2):
    """Finds the union of summarizer models for two languages using a compact data structure."""

    models1 = set(get_language_config(lang1).get("supported_models",[]))  # Get models for lang1, default to empty if not found
    models2 = set(get_language_config(lang2).get("supported_models",[]))  # Get models for lang2, default to empty if not found
    union_models = list(models1.intersection(models2))
    return union_models


def get_sources_config(filename):
    with open(filename, 'r') as file:
        sources_config = json.load(file)
    return sources_config


def publish(sources_config, lang_config, finder_template, \
        summarizer_template, html_filename, rss_filename, section_key, persona_type):        
    article_dict = {}

    for source_config in sources_config:
        try:
            logging.info(source_config["source"])

            try:
                all_links = link_cache[source_config["source_url"]]
            except KeyError:
                all_links = func_timeout(200,fetch_content,\
                        (source_config["source_url"],"links",source_config["source_language"]))
                link_cache[source_config["source_url"]] = all_links

            finder_model = random.choice(get_finder_models(source_config["source_language"]))
            best_links = get_smart_answer(
                finder_template.render(**locals()),\
                all_links,\
                finder_model, \
                "url")
            logging.info(best_links)
            link = best_links[0]

            try:
                article_text = article_cache[link]
            except KeyError:
                article_text = func_timeout(200,fetch_content,\
                        (link,source_config["source_parser"],lang_config["publishing_language"]))
                article_cache[link] = article_text

            summarizer_model = random.choice(get_summarizer_models(source_config["source_language"],lang_config["publishing_language"]))
            article_summary = get_smart_answer(
                    summarizer_template.render(**locals()),\
                    article_text,\
                    summarizer_model,\
                    "html")
            logging.info(article_summary)
            
            if not validate_article_html(article_summary,\
                    lang_config["publishing_language_short"],\
                    3):
                logging.info("Invalid article, skipping")
                raise Exception("Invalid article")

            article_title, article_summary, front_page_score, article_id = add_required_html(\
                                                                article_summary,\
                                                                link,\
                                                                source_config,\
                                                                lang_config,\
                                                                finder_model,\
                                                                summarizer_model)
            
            article_dict[article_title] = {}
            article_dict[article_title]["html"] = article_summary
            article_dict[article_title]["score"] = front_page_score
            article_dict[article_title]["id"] = article_id
            logging.info(article_summary)
        except FunctionTimedOut:    
            logging.info("Function timed out")
            logging.error("Exception occurred", exc_info=True)
        except Exception as e:
            logging.error(f"Failed to summarize {source_config['source']}")
            logging.exception(f"An unexpected error occurred, ignoring: {e}")
            logging.error("Exception occurred", exc_info=True)
    
    try:
        ads = get_available_ads(lang_config["publishing_language_short"])
        if len(ads) > 0:
            ad = random.choice(ads)
            article_title, article_summary, front_page_score, article_id = add_required_html(\
                                                                ad[lang_config["publishing_language_short"]],\
                                                                ad["url"],\
                                                                ad,\
                                                                lang_config,\
                                                                "Hard-Coded",\
                                                                "Hard-Coded")
            
            article_dict[article_title] = {}
            article_dict[article_title]["html"] = article_summary
            article_dict[article_title]["score"] = front_page_score
            article_dict[article_title]["id"] = article_id
    except Exception as e:
        logging.exception(f"An unexpected error occurred, ignoring: {e}")
        logging.error("Exception occurred", exc_info=True)
   
    sorted_articles = sorted(article_dict.items(), key=lambda x: (x[1]['score'], random.random()), reverse=True)
    article_html=""
    article_rss=""
    for article_title, article_data in sorted_articles:
        if article_data['score'] <= 1:
            logging.info("Filtering out bad article: " + article_title)
        else:
            article_html += article_data['html']
            article_rss += f"""
                            <item>
                              <title>{article_title}</title>
                              <link>https://translatetribune.com/{html_filename}#{article_data['id']}</link>
                              <guid isPermaLink="false">https://translatetribune.com/{html_filename}#{article_data['id']}</guid>
                              <description>
                                <![CDATA[
                                  {simplify_html(article_data['html'])}    
                                ]]>
                              </description>
                              <pubDate>{datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")}</pubDate>
                            </item>
                                """

    complete_html = deploy_website(article_html, html_filename,\
                                   article_rss, rss_filename,\
                                   lang_config, section_key)
    logging.info(complete_html)


def deploy_language(publishing_language):
    lang_config = get_language_config(publishing_language)
    
    finder_template = load_template('config/finder.txt')
    summarizer_template = load_template('config/summarizer.txt')
    
    debug = os.environ.get('DEBUG', False)
    sources_filename = 'config/sources_debug.json' if debug else 'config/sources_geopolitics.json'
    
    publish(get_sources_config(sources_filename),\
            lang_config,\
            finder_template,\
            summarizer_template,\
            f'{lang_config["publishing_language_short"]}.html',\
            f'{lang_config["publishing_language_short"]}.xml',\
            "geopolitics",\
            "geopolitics_persona")

    # Copy assets to debug folder
    if debug:
        assets_source_folder = '/usr/src/app/static/assets'
        assets_destination_folder = '/usr/src/app/debug/assets'
        if os.path.exists(assets_destination_folder):
            shutil.rmtree(assets_destination_folder)
        shutil.copytree(assets_source_folder, assets_destination_folder)
       

    # Create the technology page
    if not debug:
        publish(get_sources_config('config/sources_tech.json'),\
                lang_config,\
                finder_template,\
                summarizer_template,\
                f'{lang_config["publishing_language_short"]}-ft.html',\
                f'{lang_config["publishing_language_short"]}-ft.xml',\
                "tech",\
                "tech_persona")

if __name__ == "__main__":
    debug = os.environ.get('DEBUG', False)
    
    if debug:
        #deploy_language("Arabic")
        deploy_language("English")
        deploy_language("Hungarian")
    else:
        with open('config/languages.json', 'r') as file:
            lang_configs = json.load(file)
        
        for lang_config in lang_configs:
            deploy_language(lang_config["publishing_language"])
