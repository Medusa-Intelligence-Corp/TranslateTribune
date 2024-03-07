# TranslateTribune

Welcome to the source code for [https://TranslateTribune.com](https://translatetribune.com), a project dedicated to breaking down language barriers and providing a daily dose of global insights. Our mission is to curate and translate news from a broad array of countries, both friendly and hostile to the US, making international news accessible to English-speaking audiences.

## Motivation

Access to diverse perspectives is crucial for a comprehensive understanding of global events, yet language barriers and media biases often limit our exposure. TranslateTribune aims to bridge this gap by leveraging advanced AI technology to select, translate, and summarize news articles from around the globe, offering a more nuanced view of international affairs.

Our initiative recognizes that mainstream news, particularly in countries like the US, is frequently influenced by a narrow set of corporations and viewpoints. To truly grasp global complexities, it's essential to explore voices beyond these dominant narratives, especially those from the "global south," which are often overlooked in English-speaking mainstream media.

A key motivation for TranslateTribune is to provide access to original news content in its native language, such as articles from the People's Daily in China, translated to preserve the original context and meaning. This approach ensures that our users can engage with content that might be altered or 'sanitized' for international audiences. We aim to offer translations from various sources worldwide, enabling users to hear directly from local perspectives on important issues, from regional conflicts to economic policies.

TranslateTribune is designed to complement your primary news sources. It serves as a tool for those seeking to broaden their understanding with direct insights from the countries and communities at the heart of global stories. Whether it's gaining insight into Israel's stance on its conflicts or the Communist Party's views on China's economy, TranslateTribune facilitates direct access to these viewpoints, promoting a more informed and diverse global discourse.

TranslateTribune is about removing barriers—linguistic, cultural, and ideological—to help users become more informed global citizens. By providing access to a broader array of news sources, we aim to contribute to a more empathetic and connected world.

## How It Works

TranslateTribune leverages State of the art LLMs, Python, Selenium WebDriver via Docker, and Beautiful Soup 4 (bs4) to:

- Read foreign language news sites from a wide range of countries.
- Use AI to pick relevant news articles.
- Translate and summarize these articles into English.

Our process ensures that you get accurate, concise summaries of international news, offering insights into how different cultures and countries report on similar events or issues.

## Features

- **Daily Updates:** Fresh news summaries every day, giving you a constant stream of global insights.
- **Diverse Sources:** Articles are selected from a variety of countries and perspectives, ensuring a well-rounded view of world events. (see [sources.json](./sources.json))
- **AI-Powered Summaries:** Quick, accurate translations and summaries powered by the latest AI technology.

## Getting Started

To explore our project and start reading the summaries, visit our GitHub repository. We welcome feedback and contributions to help expand our coverage and improve our translations.

To run the scraper and generate an index.html to the console do the following:
* ```git clone``` this repo
* ```bash build.sh``` to build the docker container
* ```bash run.sh``` to run the curation and translation job

If you'd like to edit the code note the following structure:
* [```publisher.py```](./publisher.py) is the main loop that controls the job
* [```browser.py```](./browser.py) is how text is extracted from sites
* [```llm.py```](./llm.py) handles any LLM connections and formatting
* [```templater.py```](./templater.py) creates the index.html and deploys it to AWS s3

## Contributing

We're always looking for volunteers to help with:

- Identifying new sources to scrape.
- Improving our AI models for more accurate translations and summaries.
- Enhancing our web scraping capabilities.

If you're interested in contributing, please check out our contributing guidelines or contact us directly.

## License

TranslateTribune is open-source and available under the GPLv3 License. See the LICENSE file for more details.

## Contact

For more information, questions, or to get involved, please see [https://medusaintel.co](https://medusaintel.co) or email [editor@translatetribune.com](mailto:editor@translatetribune.com).

Join us in our mission to make global news accessible to everyone, regardless of language barriers. Together, we can gain a deeper understanding of the world around us.

## TODO 
- [ ] Upgrade Claude API keys to production AND/OR add OpenAI GPT-4 Turbo
- [ ] New sections for Economy, Technology, US News
- [ ] Properly market/share
- [ ] Solicit donations and no-tracker honor-system subscriptions (via coinbase and patreon)
