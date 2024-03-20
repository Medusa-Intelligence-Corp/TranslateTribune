import os
import re
import json
import logging

import validators

import anthropic

import openai

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from urlextract import URLExtract

from bs4 import BeautifulSoup

model_urls={
    "Claude 3o":"https://www.anthropic.com/claude",
    "Claude 3h":"https://www.anthropic.com/claude",
    "Claude 2.1":"https://www.anthropic.com/news/claude-2-1",
    "GPT-4":"https://openai.com/research/gpt-4",
    "GPT-3.5t":"https://openai.com/blog/gpt-3-5-turbo-fine-tuning-and-api-updates",
    "Mistral-LG":"https://mistral.ai/news/mistral-large/",
    "Mistral-MD":"https://docs.mistral.ai/guides/model-selection/",
    "Mistral-SM":"https://docs.mistral.ai/guides/model-selection/",
    "Open Mixtral":"https://mistral.ai/news/mixtral-of-experts/"
    }


def text_to_chunks(text, chunk_size=175000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


def find_urls(text):
    extractor = URLExtract()
    potential_urls = extractor.find_urls(text, check_dns=True)
    valid_urls = [url for url in potential_urls if validators.url(url)]
    return valid_urls


def find_html(text):
    soup = BeautifulSoup(text, 'html.parser')

    largest_block = None
    largest_size = 0

    for element in soup.children:
        if element.name and len(list(element.descendants)) > largest_size:
            largest_block = element
            largest_size = len(list(element.descendants))

    if largest_block:
        return largest_block.prettify()
    else:
        return ""


def validate_article_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    article_div = soup.find('div', class_='article')
    if not article_div:
        return False

    article_title_div = article_div.find('div', class_='article-title')
    if not article_title_div:
        return False

    article_content_p = article_div.find('div', class_='article-content hidden')
    if not article_content_p:
        return False

    return True


def find_json(text):
    json_match = re.search(r'({.*})', text, re.DOTALL)

    if json_match:
        json_str = json_match.group(1)
        try:
            return json.loads(json_str)
        except Exception:
            return []
    else:
        return [] 
    
def send_to_anthropic(text_chunk, instructions, model_id="claude-3-opus-20240229"):
    client = anthropic.Anthropic()

    message = client.messages.create(
        model=model_id,
        max_tokens=4000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{instructions}\n\n{text_chunk}"
                    }
                ]
            }
        ]
    )
    
    return message.content[0].text


def send_to_openai(text_chunk, instructions, model_id="gpt-4-turbo-preview"):
    client = openai.OpenAI()

    chat_completion = client.chat.completions.create(
    model=model_id,
    messages=[
            {
                "role": "user",
                "content": f"{instructions}\n\n{text_chunk}"
            }
        ]
    )

    return chat_completion.choices[0].message.content


def send_to_mistral(text_chunk, instructions, model_id="mistral-large-latest"):
    client = MistralClient(
            api_key=os.environ["MISTRAL_API_KEY"]
            )

    chat_completion = client.chat(
    model=model_id,
    messages=[ChatMessage(
            role="user",
            content=f"{instructions}\n\n{text_chunk}"
            )
        ]
    )

    return chat_completion.choices[0].message.content


def fetch_llm_response(text, instructions, model, validation=None):

    if model == "Claude 3o":
        chunks = text_to_chunks(text,chunk_size=(190000-len(instructions)))
        response = send_to_anthropic(chunks[0], instructions)
    elif model == "Claude 3h":
        chunks = text_to_chunks(text,chunk_size=(190000-len(instructions)))
        response = send_to_anthropic(chunks[0], instructions,'claude-3-haiku-20240307')
    elif model == "Claude 2.1":
        chunks = text_to_chunks(text,chunk_size=(190000-len(instructions)))
        response = send_to_anthropic(chunks[0], instructions,'claude-2.1')
    elif model == "GPT-4":
        chunks = text_to_chunks(text,chunk_size=(190000-len(instructions)))
        response = send_to_openai(chunks[0],instructions)
    elif model == "GPT-3.5t":
        chunks = text_to_chunks(text,chunk_size=(31000-len(instructions)))
        response = send_to_openai(chunks[0],instructions,'gpt-3.5-turbo')
    elif model == "Mistral-LG":
        chunks = text_to_chunks(text,chunk_size=(31000-len(instructions)))
        response = send_to_mistral(chunks[0], instructions)
    elif model == "Mistral-MD":
        chunks = text_to_chunks(text,chunk_size=(31000-len(instructions)))
        response = send_to_mistral(chunks[0], instructions,'mistral-medium-latest')
    elif model == "Mistral-SM":
        chunks = text_to_chunks(text,chunk_size=(31000-len(instructions)))
        response = send_to_mistral(chunks[0], instructions,'mistral-small-latest')
    elif model == "Open Mixtral":
        chunks = text_to_chunks(text,chunk_size=(31000-len(instructions)))
        response = send_to_mistral(chunks[0], instructions,'open-mixtral-8x7b')
    else:
        return fetch_llm_response(text, instructions, "Open Mixtral", validation) 

    if validation is None:
        return response
    elif validation == "url":
        logging.info(response)
        return find_urls(response)
    elif validation == "html":
        return find_html(response)
    elif validation == "html-article":
        html = find_html(response)
        if validate_article_html(html):
            return html
        else:
            logging.info("bad formatting from LLM")
            return None
    elif validation == "json":
        return find_json(response)
    else:
        return None


def get_model_url(model):
    return model_urls.get(model,"https://github.com/Hannibal046/Awesome-LLM")
