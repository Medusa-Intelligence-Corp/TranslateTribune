import os
import re
import json
import logging
import time

import requests
import validators

import anthropic

import openai

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

import google.generativeai as genai

from urlextract import URLExtract
from bs4 import BeautifulSoup
from langdetect import detect


class UnsupportedModelException(Exception):
    """Exception raised for unsupported models."""
    def __init__(self, model, message="Model not supported"):
        self.model = model
        self.message = message
        super().__init__(self.message)


class UnsupportedValidationException(Exception):
    """Exception raised for unsupported validation."""
    def __init__(self, validation, message="Validation type not supported"):
        self.validation = validation
        self.message = message
        super().__init__(self.message)


def text_to_chunks(text, chunk_size=175000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


def find_urls(text):
    extractor = URLExtract()
    potential_urls = extractor.find_urls(text, check_dns=True)
    valid_urls = []
    for url in potential_urls:
        if url.endswith('.'):
            url = url[:-1]
        if validators.url(url):
            valid_urls.append(url)
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


def validate_article_html(html, language_code, min_article_score, model):
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

    article_div = soup.find('div', class_='article',\
            attrs=lambda attrs: 'data-front-page-score'\
            in attrs and min_article_score <= int(attrs['data-front-page-score']) <= 5)
    if not article_div:
        return False

    article_title_div = article_div.find('div', class_='article-title')
    if not article_title_div:
        return False

    article_content = article_div.find('div', class_='article-content hidden')
    if not article_content:
        return False

    content_text = article_content.text.strip()
    llm_output_language = detect(content_text)
    logging.info(f"detected output language {llm_output_language}")
    if language_code not in llm_output_language:
        logging.info(f"Wrong Language from LLM. \
                Expected {language_code}\
                got {llm_output_language} from {model}")
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


def route_llm_prompt(text_chunk, instructions, llm_providers, source_langage, target_language):
    """
    Route the given prompt to the appropriate LLM model using Not Diamond.
    """
    nd_url = "https://not-diamond-server.onrender.com/v2/TT/translate"
    nd_api_key = os.getenv("ND_API_KEY")
    if not nd_api_key:
        logging.warning("ND_API_KEY not set. Skipping routing.")
        return None

    body = {
        "source_language": source_langage,
        "target_language": target_language,
        "messages": [{"role": "system", "content": instructions}, {"role": "user", "content": text_chunk}],
        "llm_providers": llm_providers
    }
    response = requests.post(
        nd_url,
        json=body,
        headers={
            "Authorization": f"Bearer {nd_api_key}",
            "content-type": "application/json",
        },
    )
    selected_model = response.json().get("provider").get("model")
    logging.info(f"ND routing to {selected_model} for {source_langage} to {target_language} translation.")
    return selected_model


def send_to_gemini(text_chunk, instructions, n_retries: int=3, retry_wait: float=2.0, model_id="gemini-1.0-pro-latest"):
    """
    Send a prompt to the specified model at Gemini. Retry up to n_retries times if the response is empty.
    """
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    gemini = genai.GenerativeModel(f"models/{model_id}")

    messages = [
        {"role": "user", "parts": instructions},
        {"role": "user", "parts": text_chunk}
    ]

    retries = 0
    while retries < n_retries:
        response = gemini.generate_content(
            messages,
            generation_config=genai.types.GenerationConfig(temperature=0.),
        )
        response_text = "\n".join(part.text for part in response.candidates[0].content.parts)

        if response_text:
            break
        else:
            retries += 1
            time.sleep(retry_wait)

    if response_text:
        return response_text
    raise RuntimeError(f"Failed to generate content from {model_id} after {n_retries} retries.")


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


def fetch_llm_response(text, instructions, model, validation=None, language_filter=None, min_article_score=None,source_langage=None, target_language=None):
    llm_providers = [
        {"provider": "anthropic", "model": "claude-3-haiku-20240307"},
        {"provider": "google", "model": "gemini-1.5-flash-latest"},
        # More expensive model options
        # {"provider": "google", "model": "gemini-1.5-pro-latest"},
        # {"provider": "openai", "model": "gpt-4o-2024-05-13"},
    ]

    nd_routed_model = route_llm_prompt(text, instructions, llm_providers, source_langage, target_language)

    nd_routing = False
    if nd_routed_model in ["gemini-1.5-flash-latest", "gemini-1.5-pro-latest"]:
        chunks = text_to_chunks(text,chunk_size=(31000-len(instructions)))
        # Google Gemini can occasionally return empty responses - handle this with retries and,
        # if necessary, fallback to the configured default model
        try:
            response = send_to_gemini(chunks[0], instructions, model_id=nd_routed_model)
            nd_routing = True
        except RuntimeError as e:
            logging.error(f"Error sending task to {nd_routed_model}. Falling back to {model}. {e}")
            response = fetch_llm_response_fallback(text, instructions, model, nd_routed_model)
    elif nd_routed_model == "claude-3-haiku-20240307":
        chunks = text_to_chunks(text,chunk_size=(190000-len(instructions)))
        response = send_to_anthropic(chunks[0], instructions,'claude-3-haiku-20240307')
        nd_routing = True
    elif nd_routed_model == "gpt-4o-2024-05-13":
        chunks = text_to_chunks(text,chunk_size=(31000-len(instructions)))
        response = send_to_openai(chunks[0],instructions,'gpt-4o-2024-05-13')
        nd_routing = True
    else:
        response = fetch_llm_response_fallback(text, instructions, model, nd_routed_model)

    if nd_routing:
        model = nd_routed_model

    if validation is None:
        return response, model
    elif validation == "url":
        logging.info(response)
        return find_urls(response), model
    elif validation == "html":
        return find_html(response), model
    elif validation == "html-article":
        html = find_html(response)
        if validate_article_html(html, language_filter, min_article_score, model):
            return html, model
        else:
            logging.info("bad formatting from LLM")
            return None, model
    elif validation == "json":
        return find_json(response), model
    else:
        raise UnsupportedValidationException(validation)

def fetch_llm_response_fallback(text, instructions, model, routed_model):
    if model == "Claude 3h":
        chunks = text_to_chunks(text,chunk_size=(190000-len(instructions)))
        response = send_to_anthropic(chunks[0], instructions,'claude-3-haiku-20240307')
    elif model == "GPT-4o":
        chunks = text_to_chunks(text,chunk_size=(31000-len(instructions)))
        response = send_to_openai(chunks[0],instructions,'gpt-4o')
    elif model == "Open Mixtral":
        chunks = text_to_chunks(text,chunk_size=(31000-len(instructions)))
        response = send_to_mistral(chunks[0], instructions,'open-mixtral-8x7b')
    else:
        raise UnsupportedModelException(f"Provided model={model}, ND routed model={routed_model}")
    return response