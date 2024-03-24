# TranslateTribune: Hacking the Global News Landscape.

Welcome to the source code for [https://TranslateTribune.com](https://translatetribune.com), a project dedicated to breaking down language barriers and providing a daily dose of global insights. Our mission is to curate and translate news from a broad array of countries, both friendly and hostile to the US, making international news accessible to English-speaking audiences.

## Motivation 🌍✨

**TranslateTribune** is an autonomous, open-source project that leverages AI to select, translate, and summarize news articles from around the world. It aims to:

- 🚀 Overcome language barriers and media biases
- 🌈 Highlight diverse perspectives
- 🔄 Prove the potential of self-updating, self-improving projects
- ⚖️ Demonstrate the limitations of copyright in the age of AI
- 💡 Provide an alternative to expensive news subscriptions
- 🗣️ Encourage a more informed and diverse global discourse
- 🌟 Prove that open source projects that don't serve ads and don't track users can thrive

TranslateTribune offers a cost-effective way to access a wide range of viewpoints. This project tries to hack the technological, legal, psychological, and budgetary aspects of the news industry. TranslateTribune seeks to contribute to a more empathetic and connected world.

## Features

- **Daily Updates:** Fresh news summaries every morning by 6am Eastern, giving you a constant stream of global insights.
- **Diverse Sources:** Articles are selected from a variety of countries and perspectives, ensuring a well-rounded view of world events. (see [sources.json](./config/sources.json) and [sources_technology_finance.json](sources_technology_finance.json))
- **AI-Powered Summaries:** Quick, accurate translations and summaries powered by the latest AI technology.

## Development Principles

At Translate Tribune, we are dedicated to providing our users with a seamless, privacy-respecting experience while delivering accurate and concise summaries of international news. Our development philosophy is centered around several core principles:

### Privacy by Design (see [privacy.html](https://translatetribune.com/privacy.html))
- **No Cookies**: We prioritize user privacy by not using cookies. Our platform operates without tracking users' online activities or preferences.
- **Minimal JavaScript**: Our site uses only essential JavaScript for basic functionalities, avoiding the "JavaScript Trap". This ensures our site remains user-friendly without compromising on privacy.
- **No Trackers**: Translate Tribune is free from any tracking mechanisms like web beacons or analytics scripts, reinforcing our commitment to user privacy.

### Lean and Smart
- **State-of-the-Art LLMs**: Leveraging the latest in language learning models, we ensure high-quality translations and summaries. We have a preference for open models but test large froniter models that are both open and closed, see [llm.py](./utils/llm.py) for more details.
- **Efficient Tools**: Utilizing Python, Selenium WebDriver via Docker, and Beautiful Soup 4, our process is streamlined for efficiency and accuracy.
- **No Dependency on Heavy Frameworks**: Our choice to avoid complex JavaScript frameworks and tools like LangChain is intentional, aiming for a lightweight, statically hosted site that respects privacy and ensures portability.
- **Code Portability**: Our codebase is designed to be easily deployable anywhere, we are heavy users of Docker and we love container Linux.

## Getting Started 🚀

To get TranslateTribune up and running, follow these steps to run the scraper and generate the HTML for the site:

1. 📥 Clone this repository:
   ```
   git clone <repository-url>
   ```
2. 📂 Navigate to the project folder:
   ```
   cd <project-folder-name>
   ```
3. 🏗️ Build the Docker container:
   ```
   bash deploy/build.sh
   ```
4. 🌐 Run the curation and translation job:
   ```
   bash deploy/run.sh
   ```
5. 📁 Output will appear in the ```debug``` folder. If you run with AWS credentials, you can also push to S3.

### Code Structure 🛠️

If you're interested in editing the code, here's a brief overview of the project structure:

- [```publisher.py```](./utils/publisher.py): The main loop that controls the job.
- [```browser.py```](./utils/browser.py): Responsible for extracting text from sites.
- [```llm.py```](./utils/llm.py): Handles any Large Language Model (LLM) connections and formatting.
- [```templater.py```](./utils/templater.py): Creates the ```index.html``` and deploys it to AWS S3.

### Viewing Run Logs

#### Accessing Logs in Docker Volume ```tt-logs```

Quickly access logs stored in the ```tt-logs``` Docker volume:

1. **Check Volume**: Verify ```tt-logs``` exists with ```docker volume ls```.
2. **Find Mount Point**: Use ```docker volume inspect tt-logs``` to find the volume's mount point in the ```Mountpoint``` field.
3. **Access Logs**: Navigate to the mount point and use ```less``` or ```tail -f``` to view ```publisher.log``` (or your specific log file).

Example to view logs:
```bash
less /var/lib/docker/volumes/tt-logs/_data/publisher.log
```
Or, to follow logs in real-time:
```bash
tail -f /var/lib/docker/volumes/tt-logs/_data/publisher.log
```

## LLM API Costs

This project utilizes various AI APIs (see [llm.py](./utils/llm.py)), each with different pricing models. Here's a breakdown of the current costs and usage:

1. **Mistral AI** ([Usage Dashboard](https://console.mistral.ai/usage/))
   - Current cost: About $0.18 per day.
   - Mistral (particularly Open Mixtral 8x7) provides powerful AI capabilities at an affordable price point.
   - Primarily used for European languages (Spanish, Portuguese, Dutch, Swedish, German, French, Polish, Ukrainian and Russian). See [sources.json](./config/sources.json) for details.

2. **Anthropic** ([Usage Logs](https://console.anthropic.com/settings/logs))
   - Current cost: Free (evaluation phase), if we were paying it'd be well under $1 per day.
   - Primarily using Claude 3 (haiku) for its strong performance.
   - Waiting on Anthropic's sales team to get me a contract, I'm probably low on their list given my teensy usage.
   - Primarily used for Asian, African and Middle-Eastern Languages (Mandarin, Korean, Japanese, Arabic, Persian, Turkish, Hebrew and Swahili). See [sources.json](./config/sources.json) for details.

3. **OpenAI** ([Usage Dashboard](https://platform.openai.com/usage))
   - Current cost: $0 (not actively using)
   - GPT-3.5 turbo underperforms compared to Mistral's open model, which is also cheaper.
   - GPT-4 provides OK results but is significantly more expensive than Claude 3 (haiku), which is fantastic.

We continuously monitor and evaluate the cost-effectiveness and performance of each API to optimize our spending while delivering high-quality results. As the project evolves, we may adjust our usage based on the specific requirements and budget constraints.

## Sister Projects

In addition to this core repository, TranslateTribune uses the following repos to help create our site.

* [https://github.com/Medusa-ML/Epub-Summarizer](https://github.com/Medusa-ML/Epub-Summarizer)
* [https://github.com/predbrad/Couch-Picross](https://github.com/predbrad/Couch-Picross)

## License 📜

**TranslateTribune** is proudly open-source and is distributed under the **GPLv3 License**. For more information, please refer to the [LICENSE](./LICENSE) file in this repository.

Additionally, the name "TranslateTribune" is a registered trademark under Code 41: Newspaper Publishing, owned by [Medusa Intelligence Corporation](https://medusaintel.co). 🛡️

## Get Involved 🤝

Interested in contributing or have questions? We'd love to hear from you! Here's how you can reach out or get involved:

- **Website**: To join or discord see the hompeage for [Medusa Intelligence Corporation](https://medusaintel.co).
- **Email**: Send your inquiries or thoughts to [editor@translatetribune.com](mailto:editor@translatetribune.com).

Join our mission to break down language barriers and make global news accessible to all. Together, we can foster a deeper understanding of our world. 🌐

## Brad's Wishlist 🌟

Here's a list of enhancements and additions Brad is looking to implement. Contributions and support in these areas are highly appreciated:

- [ ] **Foreign Language Editions** ($120/language): Expand the site to include editions in other languages, such as Chinese, to scrape US and other sources. Looking for 'editors' to manage these sources and serve as daily readers/testers.
  
- [ ] **.onion Service Setup** ($360/yr): Establish a .onion version of the site on a Vultr server using [EOTK](https://github.com/alecmuffett/eotk) (see [this guide](https://shen.hong.io/making-websites-on-tor-using-eotk/)). Alternatively, consider the [torwebsite container](https://github.com/3xploitGuy/torwebsite) for a potentially better fit with the small deployment size.
  
- [ ] **Stable Diffusion Generated Images** ($1000+/yr): Incorporate images generated by Stable Diffusion to enrich content. This would involve using the [Stable Diffusion API](https://platform.stability.ai/docs/api-reference#tag/Generate).

Your support in bringing these projects to life would be invaluable in enhancing the platform's reach and capabilities.    

## TODO (for Tanner)
- [ ] Setup your own MistralAI keys (Skip Anthropic and OpenAI for now).
- [ ] Download docker, run the project, be able to get simple output.
- [ ] In your local run, add some new sources to your sources_debug.json and make sure they produce new articles. Also make sure you can see what's happening in the logs, see [config](./config).
- [ ] Conduct prompt engineering: experiment, refine, and enhance LLM instructions (see [summarizer.txt](./config/summarizer.txt) and [finder.txt](./config/finder.txt)).
- [ ] Implement a regional filter on the homepage (Asia, Europe, etc...) see [index.html](./static/index.html).
- [ ] Add Google Gemini models and add them as an option in [llm.py](./utils/llm.py). Test and see if they can beat the current defaults given the cost.
- [ ] Add a bluesky bot integration that shares the top story to bluesky using their [Python API](https://atproto.blue/en/latest/).

