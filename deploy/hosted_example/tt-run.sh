#!/bin/bash

podman pull ghcr.io/medusa-intelligence-corp/translatetribune:latest
podman container prune -f
podman volume rm tt-logs 
podman run -d -e ANTHROPIC_API_KEY="ENTER_API_KEY_HERE" -e OPENAI_API_KEY="ENTER_API_KEY_HERE" -e MISTRAL_API_KEY="ENTER_API_KEY_HERE" -e GOOGLE_API_KEY="ENTER_API_KEY_HERE" -e OPENROUTER_API_KEY="ENTER_API_KEY_HERE" -e AWS_ACCESS_KEY_ID="ENTER_API_KEY_HERE" -e AWS_SECRET_ACCESS_KEY="ENTER_API_KEY_HERE" -v tt-logs:/var/log/tt --ulimit nofile=32768 ghcr.io/medusa-intelligence-corp/translatetribune:latest

