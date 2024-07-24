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


## How do you connect to LLMs and which ones do you use? 🤔

TranslateTribune forked its original implementation of ```llm.py``` into its own project called [```smartenough```](https://pypi.org/project/smartenough/). It wraps the best cheap LLMs and makes classification and translation easy. The package is available on PyPi and can be installed via ```pip install smartenough```. We use most of the provied models in the package, and try to use the most free and open models available.

