# How TranslateTribune Uses Web Scraping Technology 🌐🕷️

TranslateTribune is a news aggregator that translates and summarizes web content, which we believe falls under fair use. 🙏 We strive to comply with the law and respect publishers' requests not to scrape their content. Our summaries are similar to social media posts about articles but in different languages. 🌍 We always link to our sources and never post full articles. 🔗

Our scraper respectfully checks robots.txt preferences, avoids using hacks to bypass paywalls (e.g., we don't use [bypass-paywalls-chrome-clean](https://gitlab.com/magnolia1234/bypass-paywalls-chrome-clean)), identifies itself as "TranslateTribune", and uses caching to minimize bandwidth usage. 🤖 You will typically see under 5 visits from our scraper per day. 📅

<<<<<<< HEAD
## Is it social media?

Read below and decide.

### The Economist LinkedIn Post

Here's a linkedin post referencing an article in the Economist:

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
### The Economist TranslateTribune Post

Note it's in Spanish, **our posts are always both translated and summarized**.

```
🇬🇧 Inteligencia artificial transformará la salud

Priscilla Chan y Mark Zuckerberg de Chan Zuckerberg Initiative se proponen erradicar enfermedades con la ayuda de la inteligencia artificial, con un enfoque tecnológico destacado desde 2020. La ambiciosa meta de prevenir, curar o controlar todas las enfermedades parece cada vez más alcanzable con la IA.
The Economist (https://www.economist.com/technology-quarterly/2024/03/27/ais-will-make-health-care-safer-and-better)
```

## TranslateTribune Scraper Workflow
=======
We reference your site for every article we summarize and post, and probably drive traffic to your site (check your logs for ```referer="translatetribune.com"```). 📈 If you really don't want us to share one of your articles per language per day, then just ask us, but considering we are only stealing top stories we can probably find other sources easily and help them out. 🤝 Either way we're happy to talk to you and help you out, but we are unwilling and unable to pay to license your content. 💸

## TranslateTribune Scraper Workflow 🛠️
>>>>>>> 2c2e086 (better scraping doc)

The [TranslateTribune scraper code (browser.py)](./utils/browser.py) works as follows:

1. Sets custom User-Agent header to identify as "TranslateTribune/1.0" 🆔
2. Fetches robots.txt from domain and checks permission to access target URL 🤖
3. Uses Selenium with headless Chrome to load full page 🌐
4. Extracts page content for further processing 📜
5. Caches scraped result temporarily (few hours) 🗃️

# Protecting Your News Site from Web Scraping 🛡️

To make it harder for scrapers to bypass your paywall and access articles, consider these best practices:

## 1. Implement a Sophisticated Paywall 🔒
- Require user login and authentication for full articles 🔑
- Detect and block suspicious activity (e.g., abnormally fast page views from an IP) 🚨
- Serve article text and media via JavaScript to prevent access by disabling JS 🚫
    - The paywalls of [nytimes.com](https://www.nytimes.com) never work [if you are browsing without JavaScript](https://medium.com/@askadork/one-neat-trick-to-bypass-nytimes-paywall-turn-off-javascript-b0bfeed7726e), making them totally ineffective against web scraping, they seem to be relying on their legalese in their [robots.txt](https://www.nytimes.com/robots.txt), even though they also publish their entire website for free on the [```.onion```](https://open.nytimes.com/https-open-nytimes-com-the-new-york-times-as-a-tor-onion-service-e0d0b67b7482) protocol so I guess if you visit that way you can use all of their articles in your bot for free? What a mess. 🤦‍♂️ This is one for the courts to figure out, but there's a better way...
    - The [wsj.com](https://www.wsj.com) has a very effective paywall that is difficult to circumvent, good job guys 👍
    - No matter what you do, if you are popular enough your paywall will probably be circumvented by a project like [bypass-paywalls-chrome-clean](https://gitlab.com/magnolia1234/bypass-paywalls-chrome-clean), but it's still worth trying to do it 'right' to make life harder for cheap bots (written by bad developers) to get your data if you don't want them to 💪

## 2. Monitor and Block Suspicious Traffic 🚫
- Log and monitor page views to detect anomalous scraping behavior 📊
- Block IPs and user agents with suspicious access patterns ⛔
- Limit the rate at which a client can access pages ⏰

## 3. Ask Politely, Suggest Legal Action Where Possible 🙏⚖️
- Send cease and desist notices to detected scrapers 📨
- You can ask us to stop by emailing [editor@translatetribune.com](mailto:editor@translatetribune.com) 📧
- Have a clear Terms of Service prohibiting scraping and unauthorized access 📜
- Ensure the scraper is located where legal action is feasible; otherwise, focus on improving your paywall or blocking traffic 🌍
