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
    - [```templater.py```](./utils/templater.py): Creates html and deploys to AWS S3
5. Output appears in the ```debug``` folder (can also push to S3 with AWS credentials)
    Access logs in the ```tt-logs``` Docker volume (**NOTE:** this directory might be different on your machine, run ```docker volume inspect tt-logs``` to confirm):
    ```bash
    less /var/lib/docker/volumes/tt-logs/_data/publisher.log
    ```
    Or, follow logs in real-time:
    ```bash
    tail -f /var/lib/docker/volumes/tt-logs/_data/publisher.log
    ```

## [```llm.py```](./utils/llm.py) 

TranslateTribune uses various AI APIs, but can also run 100% locally via ```open-mixtral-8x7b``` or other open models of similar quality.

### Where in the configs do I change the model selection?

See [sources_debug.json](./config/sources_debug.json) to change models for local testing, [sources.json](./config/sources.json) or [sources_finance_technology.json](./config/sources_finance_technology.json).

### Which models are available?

See [```llm.py```](./utils/llm.py) to see the list of supported models.

### Tell me more... 

TT (Translate Tribune) utilizes approximately 10 million tokens per day for article curation and summarization tasks (refer to [```finder.txt```](./config/finder.txt) and [```summarizer.txt```](./config/summarizer.txt) for prompt details). While Claude 3 Haiku generally outperforms other models in these tasks across all languages, and would only cost around $2.50 per day to publish from roughly 30 sources into 19 languages at $0.25 per million tokens, Anthropic's closed models and cumbersome API access approval process pose significant challenges.

As strong advocates for free and open software, we strive to use it whenever possible. With this philosophy in mind, TT is designed to be model-agnostic and supports various popular model providers. Moreover, TT has been rigorously tested using exclusively free and open models, such as [```open-mixtral-8x7b```](https://huggingface.co/mistralai/Mixtral-8x7B-v0.1), enabling it to run on consumer hardware from anywhere in the world without requiring approval from any company or government.

While we do not condone copyright infringement, we believe that our approach of consistently translating, summarizing, providing links to source material, and maintaining transparency through our free and open codebase places us on the right side of the law and any ethical debates. However, we also recognize that ethics can be subjective and often nonsensical. We refuse to be held hostage by any company or government's half-baked ethical theories regarding our work. Instead, we remain committed to our mission of providing accessible and open language translation and summarization services.


## LLM API Docs and Usage Notes 

1. **Mistral AI** ([Usage](https://console.mistral.ai/usage/)) 🌬️
   - Very good at European languages 🇪🇺
   - Free and open-source models available 🆓

2. **Anthropic** ([Usage](https://console.anthropic.com/settings/logs)) 🤖
   - Free Evaluation Period 🎉
   - Very good at Asian languages
   - Cheapest acceptable model available via API @ $ USD 0.25 per 1M tokens
   - Annoying application/approval process 😒

3. **OpenAI** ([Usage](https://platform.openai.com/usage)) 🧠
   - $50 in free credits 💰

4. **together.ai** ([Usage](https://api.together.xyz/settings/billing)) 🤝
   - $25 in free credits 💸
   - Free and open-source models available 🆓

5. **cohere** ([Usage](https://dashboard.cohere.com/billing)) 🧩
   - $25 in free credits 💳
   - Annoying application/approval process 😕

6. **Not Diamond** ([Usage](https://app.notdiamond.ai/usage)) 💎
   - First 100,000 in query routing free 🎁
