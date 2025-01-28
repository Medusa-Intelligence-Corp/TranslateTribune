#!/bin/bash

docker pull ghcr.io/medusa-intelligence-corp/translatetribune:latest
docker container prune -f
if docker volume ls -q | grep -q "^tt-logs$"; then
    docker volume rm tt-logs
fi
docker run -d -e ANTHROPIC_API_KEY="ENTER_API_KEY_HERE" -e OPENAI_API_KEY="ENTER_API_KEY_HERE" -e MISTRAL_API_KEY="ENTER_API_KEY_HERE" -e GOOGLE_API_KEY="ENTER_API_KEY_HERE" -e OPENROUTER_API_KEY="ENTER_API_KEY_HERE" -e AWS_ACCESS_KEY_ID="ENTER_API_KEY_HERE" -e AWS_SECRET_ACCESS_KEY="ENTER_API_KEY_HERE" -v tt-logs:/var/log/tt --ulimit nofile=32768 ghcr.io/medusa-intelligence-corp/translatetribune:latest

