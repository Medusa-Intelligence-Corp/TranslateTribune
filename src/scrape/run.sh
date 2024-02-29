#!/bin/bash

docker run -it -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY -e OPENAI_API_KEY=$OPENAI_API_KEY --ulimit nofile=32768 tt-scraper
