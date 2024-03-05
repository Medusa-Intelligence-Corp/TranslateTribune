#!/bin/bash

docker run -it -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY -e OPENAI_API_KEY=$OPENAI_API_KEY -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY --ulimit nofile=32768 predbrad/translatetribune:0.0.1
