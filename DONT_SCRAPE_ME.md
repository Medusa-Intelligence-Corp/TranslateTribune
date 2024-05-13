# How TranslateTribune Uses Web Scraping Technology 🌐🕷️

TranslateTribune is a news aggregator that translates and summarizes web content, which we believe falls under fair use. 🙏 We strive to comply with the law and respect publishers' requests not to scrape their content. Our summaries are similar to social media posts about articles but in different languages. 🌍 We always link to our sources and never post full articles. 🔗

Our scraper respectfully checks robots.txt preferences, avoids using hacks to bypass paywalls (e.g., we don't use [bypass-paywalls-chrome-clean](https://gitlab.com/magnolia1234/bypass-paywalls-chrome-clean)), identifies itself as "TranslateTribune", and uses caching to minimize bandwidth usage. On a huge news day you might see under 5 visits from our scraper per day, if any. We only publish one article per source country per day and have many sources (see [sources.json](./config/sources.json) and [sources_finance_technology.json](./config/sources_finance_technology.json)).

We reference your site for every article we summarize and post, and probably drive traffic to your site (check your logs for ```referer="translatetribune.com"```). 📈 If you really don't want us to share one of your articles per language per day, then just ask us, but considering we are only stealing top stories we can probably find other sources easily and help them out. 🤝 Either way we're happy to talk to you and help you out, but we are unwilling and unable to pay to license your content. 💸

## TranslateTribune Scraper Workflow 🛠️

The [TranslateTribune scraper code (browser.py)](./utils/browser.py) works as follows:

1. Sets custom User-Agent header to identify as "TranslateTribune/1.0" 🆔
2. Fetches robots.txt from domain and checks permission to access target URL 🤖
3. Uses Selenium with headless Chrome to load full page 🌐
4. Extracts page content for further processing 📜
5. Caches scraped result temporarily (few hours) 🗃️

# Is Translate Tribune social media?

It is an open-source project where anyone can contribute sources. Compare the posts below and decide for yourself:

Here's a LinkedIn post referencing an article in the Economist:

```
🚨 Hot off the presses 🚨

Thrilled to share our latest piece in The Economist where Madeleine Daepp and I delve into the urgent challenges and implications of generative AI in disinformation campaigns. 🌐✍️
Based on our fieldwork in Taiwan during their January presidential election, we provide a firsthand look at how

(a) generative AI fuels generative propaganda, which is a bigger problem than deepfakes,
(b) generative propaganda is following the flow of online attention to short-form video on platforms like #TikTok (and monitoring narratives on these platforms is hard),
(c) it comes in waves, particularly when people are searching for real-time news on these platforms about political events as they are occurring.

In a historic year of global elections, when generative AI is developing so quickly, it is critical that governments, tech companies, and civil society work together to develop countermeasures to AI-powered disinformation.

🔗 Full article: https://lnkd.in/gubDiC8d
#Disinformation #GenerativeAI #Deepfakes #DigitalIntegrity #PublicPolicy #ElectionSecurity

Special thanks to support and advice from Eric Horvitz, Vickie Wang 王宇平, Whitney Hudson, Weishung L., Christopher White, Jonathan Larson and many others.
```

Here's a TranslateTribune referencing an article in the Economist. Note it's in Spanish. **Our posts are always both translated and summarized**.

```
🇬🇧 Inteligencia artificial transformará la salud

Priscilla Chan y Mark Zuckerberg de Chan Zuckerberg Initiative se proponen erradicar enfermedades con la ayuda de la inteligencia artificial, con un enfoque tecnológico destacado desde 2020. La ambiciosa meta de prevenir, curar o controlar todas las enfermedades parece cada vez más alcanzable con la IA.
The Economist (https://www.economist.com/technology-quarterly/2024/03/27/ais-will-make-health-care-safer-and-better)
```

# Protecting Your News Site from Web Scraping 🛡️

To make it harder for scrapers to bypass your paywall and access articles, consider these best practices:

## 1. Implement a Sophisticated Paywall 🔒
- Require user login and authentication for full articles 🔑
- Detect and block suspicious activity (e.g., abnormally fast page views from an IP) 🚨
- Serve article text and media via JavaScript to prevent access by disabling JS 🚫
    - The [nytimes.com](https://www.nytimes.com) paywall will never work [if you are browsing without JavaScript](https://medium.com/@askadork/one-neat-trick-to-bypass-nytimes-paywall-turn-off-javascript-b0bfeed7726e), making it totally ineffective against web scraping, they seem to be relying on their legalese in their [robots.txt](https://www.nytimes.com/robots.txt), even though they also publish their entire website for free on the [```.onion```](https://open.nytimes.com/https-open-nytimes-com-the-new-york-times-as-a-tor-onion-service-e0d0b67b7482) protocol
    - The [wsj.com](https://www.wsj.com) has a very effective paywall that is difficult to circumvent, good job guys 👍
    - Most news sites are still written give their content away for free to other aggregators, like Google, and if your site is written to give it away to one aggregator... your content can then be 'stolen' by all aggregators (otherwise aren't you supporting a monopoly in search? maybe).
    - No matter what you do, if you are popular enough your paywall will probably be circumvented by [one of the many paywall bypassing projects](https://github.com/search?q=bypass+paywalls&type=repositories), but it's still worth trying to do it 'right' to make life harder for cheap bots (written by bad developers) to get your data if you don't want them to 💪

## 2. Monitor and Block Suspicious Traffic 🚫
- Log and monitor page views to detect anomalous scraping behavior 📊
- Block IPs and user agents with suspicious access patterns ⛔
- Limit the rate at which a client can access pages ⏰

## 3. Ask Politely, Suggest Legal Action Where Possible 🙏⚖️
- Send cease and desist notices to detected scrapers 📨
- You can ask us to stop by emailing [editor@translatetribune.com](mailto:editor@translatetribune.com) 📧
- Have a clear Terms of Service prohibiting scraping and unauthorized access 📜
- Ensure the scraper is located where legal action is feasible; otherwise, focus on improving your paywall or blocking traffic 🌍
