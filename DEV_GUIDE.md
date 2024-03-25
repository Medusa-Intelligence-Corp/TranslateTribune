## Getting Started 🏁

1. Clone the repository
2. Navigate to the project folder
3. Build the Docker container: ```bash deploy/build.sh```
4. Run the curation and translation job: ```bash deploy/run.sh``` which uses the following:
    - [```publisher.py```](./utils/publisher.py): Main job control loop
    - [```sources.json```](./config/sources.json): Source site configuration
    - [```browser.py```](./utils/browser.py): Extracts text from sites
    - [```finder.txt```](./config/finder.txt): Prompt for finding articles to translate
    - [```summarizer.txt```](./config/summarizer.txt): Prompt for summarizing and ranking articles
    - [```llm.py```](./utils/llm.py): Handles LLM connections and formatting
    - [```templater.py```](./utils/templater.py): Creates ```index.html``` and deploys to AWS S3
5. Output appears in the ```debug``` folder (can also push to S3 with AWS credentials)
    Access logs in the ```tt-logs``` Docker volume (**NOTE:** this directory might be different on your machine, run ```docker volume inspect tt-logs``` to confirm):
    ```bash
    less /var/lib/docker/volumes/tt-logs/_data/publisher.log
    ```
    Or, follow logs in real-time:
    ```bash
    tail -f /var/lib/docker/volumes/tt-logs/_data/publisher.log
    ```

## LLM API Costs 💸 and Info

TranslateTribune uses various AI APIs with different pricing models:
1. **Mistral AI** ([Usage Dashboard](https://console.mistral.ai/usage/)): ~$0.18/day, primarily for European languages (see [sources.json](./config/sources.json))
2. **Anthropic** ([Usage Logs](https://console.anthropic.com/settings/logs)): <$1/day, primarily for Asian, African, and Middle-Eastern languages (see [sources.json](./config/sources.json))
3. **OpenAI** ([Usage Dashboard](https://platform.openai.com/usage)): Implemented and tested but not using currently.

