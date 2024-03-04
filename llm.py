import validators

from urlextract import URLExtract

from bs4 import BeautifulSoup

from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT


class UnsupportedModelException(Exception):
    def __init__(self, model, message="Model not supported"):
        self.model = model
        self.message = message
        super().__init__(self.message)


def text_to_chunks(text, chunk_approx_tokens, avg_token_length):

    chunk_approx_chars = chunk_approx_tokens * avg_token_length
    chunks = []
    text_length = len(text)
    start_index = 0

    while start_index < text_length:
        end_index = min(start_index + chunk_approx_chars, text_length)
        chunk = text[start_index:end_index]
        chunks.append(chunk)
        start_index = end_index

    return chunks


def find_urls(text):
    extractor = URLExtract()
    potential_urls = extractor.find_urls(text, check_dns=True)
    valid_urls = [url for url in potential_urls if validators.url(url)]
    return valid_urls


def find_html(text):
    main_content = BeautifulSoup(text, 'html.parser')

    if main_content:
        html_code = main_content.prettify()
        return html_code
    else:
        return ""

def send_to_anthropic(text_chunk, instructions):
    anthropic = Anthropic()

    completion = anthropic.completions.create(
        model="claude-2.1",
        max_tokens_to_sample=200000,
        prompt=f"{HUMAN_PROMPT} {instructions}:\n{text_chunk}{AI_PROMPT}",
    )

    return completion.completion


def fetch_llm_response(text, instructions, model, chunk_approx_tokens, avg_token_length, validation=None):

    if model == "Claude 2":
        chunks = text_to_chunks(text,100000,avg_token_length)
        response = send_to_anthropic(chunks[0], instructions)
    else:
        raise UnsupportedModelException(model)

    if validation is None:
        return response
    elif validation == "url":
        return find_urls(response)
    elif validation == "html":
        return find_html(response)
    else:
        return None

