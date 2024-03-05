import json
import random
import traceback

from browser import fetch_content
from llm import fetch_llm_response
from templater import deploy_website

if __name__ == "__main__":
    
    with open('sources.json', 'r') as file:
        data = json.load(file)

    random.shuffle(data)

    article_html = ''

    for item in data:
        try:
            name = item.get("name", "N/A")
            language = item.get("language", "N/A")
            flag = item.get("flag", "N/A")
            source = item.get("source", "N/A")
            url = item.get("url", "N/A")
            model = item.get("model", "Claude 2")
            chunk_approx_tokens = item.get("tokens", 150000)
            avg_token_length = item.get("token_length", 3)
            article_title_length = item.get("article_title_length",15)
             
                
            print(f"Name: {name}, Language: {language}, Flag: {flag}")
            print(f"Source: {source}, URL: {url}")
            print(f"Model: {model}")
            
            finder = f"""Act as a polyglot international newspaper editor who is an ex-CIA analyst, your goal is to pick the best articles to translate to English. Please review the article links and titles provided from {source}, a {language} language newspaper. Identify one article that offers unique insights or perspectives specific to the {name}, or at least an article that seems interesting to learn more about. The article will be considered for translation into English. Check any links you suggest to make sure they aren't links to files like pdfs (we don't want those). Please respond only in valid json as if you were an API.

Article list:
                """

            print("--------------------------------------------------")
            print("---------------ARTICLE-LIST-----------------------")
            print("--------------------------------------------------")
            
            all_links = fetch_content(url,"links",article_title_length) 
            if len(all_links) > 100:
                print(all_links[:100])
                print("...")
                print(all_links[-100:])

            print("--------------------------------------------------")
            print("---------------AI-CURATION------------------------")
            print("--------------------------------------------------")
            
            best_links = fetch_llm_response(
                all_links, finder, model, chunk_approx_tokens, avg_token_length, "url")
            print(best_links)
            
            if best_links is not None:
                
                for link in best_links:
                    
                    summarizer = f"""Act as a translator and summarizer. Below, I will provide the text of an article in {language}. Please, create a summary of the article's content in English. Additionally, identify and include a few key {language} vocabulary phrases that would be beneficial for a student learning {language}. The response should be formatted exclusively in valid HTML, adhering to the structure provided below:

                    return format:             
                    ```
                    <div class="article">
                        <div class="article-title">TITLE IN ENGLISH</div>
                        <div class="article-source"><span class="flag-icon">{flag}</span><a href="{link}">{source}</a></div>
                        <p class="article-content">SUMMARY IN ENGLISH (translated by {model})</p>
                        <p class="vocabulary">VOCABULARY</p>
                    </div>
                    ```

                    Please ensure that the summary provides a clear, concise overview of the article's main points, and select vocabulary words that are relevant to the article's content, potentially challenging for learners, and useful in building their language skills. The HTML output should strictly follow the provided structure, with no additional text or formatting outside of the specified HTML tags.

                        article text:
                        """
                    
                    print("--------------------------------------------------")
                    print("--------FULL-ARTICLE-TEXT-------------------------")
                    print("--------------------------------------------------")
                    
                    article_text = fetch_content(link,"text") 
                    if len(article_text) > 100:
                        print(article_text[:100])
                        print("...")
                        print(article_text[-100:])
                    
                    print("--------------------------------------------------")
                    print("----------AI-TRANSLATION-AND-SUMMARY--------------")
                    print("--------------------------------------------------")
                
                    article_summary = fetch_llm_response(
                            article_text, summarizer, model, chunk_approx_tokens, avg_token_length, "html")
                    print(article_summary)

                    article_html += "<!-- NEW ARTICLE -->"
                    article_html += article_summary

            print("--------------------------------------------------")
            print("--------------------------------------------------")
            print("--------------------------------------------------")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            traceback.print_exc()
            print("continuing anyway...")

    print("--------------------------------------------------")
    print("---------------HTML-TEMPLATING--------------------")
    print("--------------------------------------------------")
    
    indexhtml=deploy_website(article_html)
    print(indexhtml)

