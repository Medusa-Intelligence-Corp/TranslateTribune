# Use the official Selenium base image with Standalone Chrome
FROM selenium/standalone-chrome:latest

# Set working directory
WORKDIR /usr/src/app

# Install Python and pip
USER root
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    wget \
    unzip \
    xvfb

# Install the latest LTS nodejs
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs

# Install Python dependencies
RUN pip3 install --no-cache-dir \
    selenium \
    beautifulsoup4 \
    requests \
    pytz \
    cachetools \
    urlextract \
    validators \
    langdetect \
    goose3[all] \
    readabilipy \
    Jinja2 \
    bleach \
    anthropic \
    openai \
    mistralai \
    boto3 \
    google-generativeai


# Copy the rest of your application's code
COPY . .

CMD ["python3","utils/publisher.py"]
