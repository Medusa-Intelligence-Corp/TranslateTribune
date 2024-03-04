import json

from browser import fetch_content
from llm import fetch_llm_response
from templater import deploy_website

if __name__ == "__main__":
    
    with open('sources.json', 'r') as file:
        data = json.load(file)

    article_html = ""

    for item in data:
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
        
        print("--------------------------------------------------")
        print("---------------PART-1-CURATION--------------------")
        print("--------------------------------------------------")

        finder = f"""Act as a polyglot international newspaper editor, your goal is to pick the best articles to translate to English. Please review the article links and titles provided from {source}, a {language} language newspaper. Identify up to two articles that offer unique insights or perspectives specific to the {name}. These articles should be considered for translation into English. Check any links you suggest to make sure they aren't links to files like pdfs (we don't want those). Here's an example of what I'm looking for in a response: 'Based on the content, an interesting article is \"Title\" with a unique perspective on [topic]. The URL is https://...'. Thank you!"""
        print(f"Finder: {finder}")

        print("--------------------------------------------------")
        print("---------------FETCH--RESULT----------------------")
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
                print("--------------------------------------------------")
                print("-------PART-2-TRANSLATE-AND-SUMMARIZE-------------")
                print("--------------------------------------------------")
                
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
                print(f"Summarizer: {summarizer}")
                
                print("--------------------------------------------------")
                print("--------ARTICLE-FETCH-RESULT----------------------")
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

                article_html += article_summary

        print("--------------------------------------------------")
        print("--------------------------------------------------")
        print("--------------------------------------------------")

    print("--------------------------------------------------")
    print("---------------FRONT-PAGE-CREATION----------------")
    print("--------------------------------------------------")
    
    editor="""Act as an online newspaper editor for a respected global news aggregator, take the following drafthtml and make the following changes to it:

    1. Sort the articles so that the most interesting and best articles are on top.
    2. Make the titles and text formatting consistent.
    3. Remove any errors, links to homepages, or incomplete articles.
    4. Remove any articles that seem to cover the same news story and have a similar conclusion.

The response should be formatted exclusively in valid HTML and strictly follow the structure below:
    ```
    <div class="article">
        <div class="article-title"></div>
        <div class="article-source"><span class="flag-icon"></span><a></a></div>
        <p class="article-content"></p>
        <p class="vocabulary"></p>
    </div>
    ```

The response should be pure valid HTML with no additional text or formatting outside of the specified HTML tags.

Current draft HTML:

"""

    edited_html = fetch_llm_response(
            article_html, editor, "Claude 2", 150000, 3, "html")  

    if len(edited_html) > 100:
        print(edited_html[:100])
        print("...")
        print(edited_html[-100:])
    

    print("--------------------------------------------------")
    print("---------------HTML-TEMPLATING--------------------")
    print("--------------------------------------------------")
    
    indexhtml=deploy_website(edited_html)
    print(indexhtml)

