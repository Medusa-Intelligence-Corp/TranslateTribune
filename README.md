<h1 align="center">
        <img src="./static/icon.png" alt="Translate Tribune">
        <br>
        <a href="https://translatetribune.com" target="_blank">TranslateTribune</a>
    </h1>
    <p align="center">
        <p align="center">A free and open-source project that leverages LLMs (<a href="https://mistral.ai/news/mixtral-of-experts/" target="_blank">Open Mixtral</a> and <a href="https://www.anthropic.com/news/claude-3-family" target="_blank">Claude 3 Haiku</a>) to curate, translate, and summarize news articles from diverse countries. Read our daily English edition at <a href="https://translatetribune.com" target="_blank">TranslateTribune.com</a>.
        <br>
    </p>
<h4 align="center">
    <a href="https://github.com/Medusa-ML/TranslateTribune/blob/main/LICENSE" target="_blank">
        <img alt="GitHub License" src="https://img.shields.io/github/license/Medusa-ML/TranslateTribune">
    </a>
    <a href="https://github.com/Medusa-ML/TranslateTribune/actions/workflows/build-and-push.yml" target="_blank">
        <img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/Medusa-ML/TranslateTribune/build-and-push.yml">
    </a>
    <a href="https://discord.gg/bEPkfhbwE4">
        <img src="https://img.shields.io/static/v1?label=Chat%20on&message=Discord&color=blue&logo=Discord&style=flat-square" alt="Discord">
    </a>
    <a href="#project-wishlist">
    <img alt="Project Wishlist" src="https://img.shields.io/badge/%F0%9F%92%B0_Project_Wishlist-purple">
    </a>
</h4>

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
- 🔒 Private by Design: no cookies, minimial JavaScript, and no trackers. [Read our full privacy policy here.](https://translatetribune.com/privacy.html).

## Development Principles 🛠️

- **🔒 Privacy by Design**: TranslateTribune prioritizes user privacy by eschewing cookies, minimizing JavaScript, and eliminating trackers. Our commitment to privacy is outlined in our [privacy policy](https://translatetribune.com/privacy.html).
- **🚀 Lean and Portable**: Our lightweight, static site avoids heavy frameworks and excessive JavaScript. It's fully Dockerized with documented dependencies, ensuring a reproducible dev environment and easy deployment anywhere.
- **🛡️ Secure and Resilient**: We collect no user data and keep no logs. Our static architecture makes the site resilient and adaptable to a variety of hosting environments worldwide.

## Getting Started 🏁

See [DEV_GUIDE.md](./DEV_GUIDE.md)

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

## LLM API Costs 💸 and Info
TranslateTribune uses various AI APIs with different pricing models:
1. **Mistral AI** ([Usage Dashboard](https://console.mistral.ai/usage/)): ~$0.18/day, primarily for European languages (see [sources.json](./config/sources.json))
2. **Anthropic** ([Usage Logs](https://console.anthropic.com/settings/logs)): <$1/day, primarily for Asian, African, and Middle-Eastern languages (see [sources.json](./config/sources.json))
3. **OpenAI** ([Usage Dashboard](https://platform.openai.com/usage)): Implemented and tested but not using currently.

## License and Trademark 📜
TranslateTribune is free (as in speech) and open source under the [GPLv3 License](./LICENSE). The name "TranslateTribune" is a registered trademark owned by [Medusa Intelligence Corporation](https://medusaintel.co).

## Project Wishlist

Our project is fully funded for its current functionality 🙌. However, with additional support, we can enhance the project with the following features:

- [ ] **🕵️‍♂️ Improve Privacy and Security with .onion Service** ($360 per year) - Set up an .onion service using either [EOTK](https://github.com/alecmuffett/eotk) ([guide](https://shen.hong.io/making-websites-on-tor-using-eotk/)) or [torwebsite container](https://github.com/3xploitGuy/torwebsite) to enhance the privacy and security of our project.
- [ ] **🖼️ Enhance Visuals with AI-Generated Images** ($1000+ per year) - Elevate the visual appeal of our project by integrating AI-generated images using the [Stable Diffusion API](https://platform.stability.ai/docs/getting-started).

If you believe in our project and would like to contribute to its growth, you can support us through the following methods:

1. **Patreon**: Become a patron and [pledge a monthly donation of $10 via our Patreon page](https://www.patreon.com/bradflaugher). Your consistent support will help us sustain and expand the project.

2. **Coinbase**: For larger one-time donations, please consider [making a donation via Coinbase](https://commerce.coinbase.com/checkout/97bb9f4f-1736-48c7-9c68-682134c8db5c). Your generous contribution will significantly accelerate the development of new features.

Every donation, no matter the size, makes a difference and brings us closer to our goals. We appreciate your support and dedication to our project. Together, we can make a meaningful impact.

Thank you for considering supporting us!
