import os
import re
import json
import logging

import validators

import anthropic

import openai

from notdiamond.llms.llm import NDLLM
from notdiamond.prompts.prompt import NDPromptTemplate, NDContext, NDQuery

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from urlextract import URLExtract

from bs4 import BeautifulSoup




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

    article_div = soup.find('div', class_='article', \
            attrs=lambda attrs: 'data-front-page-score' in attrs and 0 <= \
            int(attrs['data-front-page-score']) <= 5)
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

def send_to_notdiamond(text_chunk, instructions):
    context = NDContext(text_chunk)
    query = NDQuery(instructions)

    prompt_template = NDPromptTemplate("{query}\n\n{context}", 
                       partial_variables={"context":context, "query": query})

    #TODO add new models here, Google, Mixtral 8x7 and Claude 3 Haiku when supported
    llm_providers = ['openai/gpt-3.5-turbo',  'anthropic/claude-2.1', 
                     'mistral/mistral-small-latest']

    nd_llm = NDLLM(llm_providers=llm_providers)

    result, session_id, provider = nd_llm.invoke(prompt_template=prompt_template)

    logging.info(f"ND session ID: {session_id}")  # Important for personalizing ND to your use-case
    logging.info(f"LLM called: {provider.model}")  
    
    return result.content
        


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
    elif model == "Not Diamond":
        chunks = text_to_chunks(text,chunk_size=(190000-len(instructions))) #NOTE this could be bigger for ND, they truncate extra data.
        response = send_to_notdiamond(chunks[0], instructions)
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
