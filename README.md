# TranslateTribune: Breaking Language Barriers in Global News 🌍📰

TranslateTribune ([https://TranslateTribune.com](https://translatetribune.com)) is an open-source project that leverages AI to curate, translate, and summarize news articles from diverse countries, making international news accessible to English-speaking audiences. 🤖🗞️

## Mission 🎯

- 🚀 Overcome language barriers and media biases
- 🌈 Highlight diverse perspectives
- 🔄 Prove the potential of self-updating, self-improving projects
- ⚖️ Demonstrate the limitations of copyright in the age of AI
- 💡 Provide an alternative to expensive news subscriptions
- 🗣️ Encourage a more informed and diverse global discourse
- 🌟 Prove that privacy-protecting free and open source projects can thrive

## Features ✨

- 📅 Daily updates by 6am Eastern
- 🌍 Diverse sources from various countries and perspectives (see [sources.json](./config/sources.json) and [sources_technology_finance.json](sources_technology_finance.json))
- 🧠 AI-powered translations and summaries

## Development Principles 🛠️

- **🔒 Privacy by Design**: TranslateTribune prioritizes user privacy by eschewing cookies, minimizing JavaScript, and eliminating trackers. Our commitment to privacy is outlined in our [privacy policy](https://translatetribune.com/privacy.html).
- **🚀 Lean and Portable**: Our lightweight, static site avoids heavy frameworks and excessive JavaScript. It's fully Dockerized with documented dependencies, ensuring a reproducible dev environment and easy deployment anywhere, including .onion sites.
- **🛡️ Secure and Resilient**: We collect no user data and keep no logs. Our static architecture makes the site resilient and adaptable to a variety of hosting environments worldwide.

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
    Access logs in the ```tt-logs``` Docker volume:
    ```bash
    less /var/lib/docker/volumes/tt-logs/_data/publisher.log
    ```
    Or, follow logs in real-time:
    ```bash
    tail -f /var/lib/docker/volumes/tt-logs/_data/publisher.log
    ```

## LLM API Costs 💸
TranslateTribune uses various AI APIs with different pricing models:
1. Mistral AI ([Usage Dashboard](https://console.mistral.ai/usage/)): ~$0.18/day, primarily for European languages (see [sources.json](./config/sources.json))
2. Anthropic ([Usage Logs](https://console.anthropic.com/settings/logs)): Free evaluation phase, primarily for Asian, African, and Middle-Eastern languages (see [sources.json](./config/sources.json))

## Sister Projects 👯‍♀️
- [https://github.com/Medusa-ML/Epub-Summarizer](https://github.com/Medusa-ML/Epub-Summarizer)
- [https://github.com/predbrad/Couch-Picross](https://github.com/predbrad/Couch-Picross)

## License 📜
TranslateTribune is open-source under the [GPLv3 License](./LICENSE). The name "TranslateTribune" is a registered trademark owned by [Medusa Intelligence Corporation](https://medusaintel.co).

## Get Involved 🤝
- Discord: [https://discord.gg/bEPkfhbwE4](https://discord.gg/bEPkfhbwE4)
- Email: [editor@translatetribune.com](mailto:editor@translatetribune.com)

## Project Wishlist (and $ required) 🧞‍♂️
- [ ] Foreign Language Editions ($120/language)
- [ ] .onion Service Setup ($360/yr) using [EOTK](https://github.com/alecmuffett/eotk) ([guide](https://shen.hong.io/making-websites-on-tor-using-eotk/)) or [torwebsite container](https://github.com/3xploitGuy/torwebsite)
- [ ] Stable Diffusion Generated Images ($1000+/yr) using [Stable Diffusion API](https://platform.stability.ai/docs/api-reference#tag/Generate)

## TODO (for Tanner) 📝
- [ ] Setup MistralAI keys
- [ ] Run the project locally, add new sources to [```sources_debug.json```](./config/sources_debug.json)
- [ ] Refine LLM instructions in [```summarizer.txt```](./config/summarizer.txt) and [```finder.txt```](./config/finder.txt)
- [ ] Implement regional filter on homepage ([```index.html```](./static/index.html))
- [ ] Add Google Gemini models to [```llm.py```](./utils/llm.py)
- [ ] Develop a Bluesky bot to share the top story(ies) from each edition (see [BlueSky Python SDK](https://atproto.blue/en/latest/))

