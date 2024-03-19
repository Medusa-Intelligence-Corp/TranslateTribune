# TranslateTribune: Hacking the Global News Landscape.

Welcome to the source code for [https://TranslateTribune.com](https://translatetribune.com), a project dedicated to breaking down language barriers and providing a daily dose of global insights. Our mission is to curate and translate news from a broad array of countries, both friendly and hostile to the US, making international news accessible to English-speaking audiences.

## Motivation

TranslateTribune is an autonomous, open-source project that leverages AI to select, translate, and summarize news articles from around the world. It aims to:

* Overcome language barriers and media biases
* Highlight diverse perspectives
* Prove the potential of self-updating, self-improving projects
* Demonstrate the limitations of copyright in the age of AI
* Provide an alternative to expensive news subscriptions
* Encourage a more informed and diverse global discourse
* Prove that open source projects that don't serve ads and don't track users can thrive.

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

## Getting Started

To explore our project and start reading the summaries, visit our GitHub repository. We welcome feedback and contributions to help expand our coverage and improve our translations.

To run the scraper and generate an index.html to the console do the following:
* ```git clone``` this repo
* ```cd``` to the project folder
* ```bash deploy/build.sh``` to build the docker container
* ```bash deploy/run.sh``` to run the curation and translation job

If you'd like to edit the code note the following structure:
* [```publisher.py```](./utils/publisher.py) is the main loop that controls the job
* [```browser.py```](./utils/browser.py) is how text is extracted from sites
* [```llm.py```](./utils/llm.py) handles any LLM connections and formatting
* [```templater.py```](./utils/templater.py) creates the index.html and deploys it to AWS s3

### Viewing Run Logs

### Accessing Logs in the Docker Volume `tt-logs`

Follow these steps to access the logs stored in the Docker volume named `tt-logs`.

#### 1. Confirm Volume Existence

First, ensure the `tt-logs` volume exists by listing all Docker volumes:

```bash
docker volume ls
```

If `tt-logs` appears in the list, you can move on to the next step.

#### 2. Locate the Volume Mount Point

To find out where the `tt-logs` volume is mounted on your host system, inspect the volume:

```bash
docker volume inspect tt-logs
```

In the output, locate the `Mountpoint` field. This field indicates the path on the host system where the volume is mounted.

#### 3. View the Logs

With the mount point identified, you can now access the logs. If, for example, the logs are stored in a file named `log.txt` within the volume, and the mount point is `/var/lib/docker/volumes/tt-logs/_data`, you can view the logs using:

```bash
less /var/lib/docker/volumes/tt-logs/_data/publisher.log
```

you can also ```tail``` the logs while a job is running like 

```bash
tail -f /var/lib/docker/volumes/tt-logs/_data/publisher.log
```

Adjust the command based on the actual log file name and its location within the volume.

## Sister Projects

In addition to this core repository, TranslateTribune uses the following repos to help create our site.

* [https://github.com/Medusa-ML/Epub-Summarizer](https://github.com/Medusa-ML/Epub-Summarizer)
* [https://github.com/predbrad/Couch-Picross](https://github.com/predbrad/Couch-Picross)

## License

TranslateTribune is open-source and available under the GPLv3 License. See the LICENSE file for more details.

The mark "TranslateTribune" is a trademark (registered under Code 41: Newspaper Publishing) of [Medusa Intelligence Corporation](https://medusaintel.co).

## Contributing and Contacting Us

For more information, questions, or to get involved, please see [https://medusaintel.co](https://medusaintel.co) or email [editor@translatetribune.com](mailto:editor@translatetribune.com).

Join us in our mission to make global news accessible to everyone, regardless of language barriers. Together, we can gain a deeper understanding of the world around us.

## TODO (for Tanner)
- [ ] Setup your own MistralAI keys (Skip Anthropic and OpenAI for now)
- [ ] Download docker, run the project, be able to get simple output.
- [ ] Test any sources that don't seem to be producting articles and see if you can deduce what is happening in the logs, see [config](./config).
- [ ] Improve scraping and isolation of article text, maybe find the div with the most text, try and scrape in 'reader mode' or use greasemonkey scripts to improve things e.g., [Greasy Fork](https://greasyfork.org/en)
- [ ] Conduct prompt engineering: experiment, refine, and enhance LLM instructions (see [publisher.py](./utils/publisher.py#L116)) also experiment with LLM configs to see which models perform best given the cost... if you'd like to try a new model feel free to add it, just follow the pattern in [llm.py](./utils/llm.py).
- [ ] Implement a regional filter on the homepage, possibly using a flag-to-region mapping approach.
- [ ] Integrate Bluesky bot for sharing top links post-publishing using their [Python API](https://atproto.blue/en/latest/).
- [ ] Explore and test new content categories for inclusion, such as US news, local news, or gaming news. Consider forking the project to experiment with these ideas.

