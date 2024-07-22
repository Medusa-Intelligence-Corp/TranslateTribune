## Getting Started 🏁

1. Clone the repository
2. Navigate to the project folder
3. Build the Podman container: ```bash deploy/build.sh```
4. Run the curation and translation job: ```bash deploy/run.sh``` which uses the following:
    - [```publisher.py```](./utils/publisher.py): Main job control loop
    - [```sources.json```](./config/sources.json): Source site configuration
    - [```browser.py```](./utils/browser.py): Extracts text from sites
    - [```finder.txt```](./config/finder.txt): Prompt for finding articles to translate
    - [```summarizer.txt```](./config/summarizer.txt): Prompt for summarizing and ranking articles
    - [```templater.py```](./utils/templater.py): Creates html and deploys to AWS S3
5. Output appears in the ```debug``` Podman volume (can also push to S3 with AWS credentials) run ```podman volume inspect tt-debug``` to find the directory on your machine.
6. Access logs in the ```tt-logs``` Podman volume (**NOTE:** this directory might be different on your machine, run ```podman volume inspect tt-logs``` to confirm):
    ```bash
    [user@code TranslateTribune]$ podman volume inspect tt-logs
    [
         {
              "Name": "tt-logs",
              "Driver": "local",
              "Mountpoint": "/home/user/.local/share/containers/storage/volumes/tt-logs/_data",
              "CreatedAt": "2024-07-22T13:07:15.15786752-04:00",
              "Labels": {},
              "Scope": "local",
              "Options": {},
              "MountCount": 0,
              "NeedsCopyUp": true,
              "NeedsChown": true,
              "LockNumber": 2
         }
    ]    
    ```

## Big-Picture Principles 🌍

* **Privacy**: We think the news that people consume is sensitive, we don't want to know what you read
* **Decentralization**: We don't want to be a single point of failure, we want to be able to run on any machine
* **Open-Source**: We want to be able to share our code with the world
* **Cheap**: We want to be able to run this on a Raspberry Pi if we have to
* **Free (as in Freedom)**: We want this to be free to use and free to modify

## Can I use Docker instead of Podman? 🐳

Yes you should be able to take any of the ```podman``` commands and replace them with ```docker``` and it should work.


## How do you connect to LLMs? 🤔

TranslateTribune forked its original implementation of ```llm.py``` into its own project called [```smartenough```](https://pypi.org/project/smartenough/). It wraps the best cheap LLMs and makes classification and translation easy. The package is available on PyPi and can be installed via ```pip install smartenough```.


## Which LLMS are you using? 🤖

1. **Mistral AI** ([Usage](https://console.mistral.ai/usage/)) 🌬️
   - Very good at European languages 🇪🇺
   - Free and open-source models available 🆓

2. **Anthropic** ([Usage](https://console.anthropic.com/settings/logs)) 🤖
   - Free Evaluation Period 🎉
   - Very good at Asian languages
   - Cheapest acceptable model available via API @ $ USD 0.25 per 1M tokens
   - Annoying application/approval process 😒

3. **OpenAI** ([Usage](https://platform.openai.com/usage)) 🧠
   - Performs decently on all languages, used for finding articles to translate
   - $50 in free credits 💰

4. **Google** ([Usage](https://console.cloud.google.com/billing/))
   - Good at Asian languages and other Non-European languages
   - First $250 in free credits

5. **OpenRouter** ([Usage](https://openrouter.io/))
   - Free ($0) and Libre/Free and open-source models available 🆓
   - They are a bit slow and not as good as Mistral AI
