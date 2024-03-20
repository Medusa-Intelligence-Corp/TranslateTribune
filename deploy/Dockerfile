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

# Install Python dependencies
RUN pip3 install --no-cache-dir \
    selenium \
    beautifulsoup4 \
    pytz \
    urlextract \
    validators \
    goose3[all] \
    Jinja2 \
    anthropic \
    openai \
    mistralai \
    boto3

# Install the latest LTS nodejs
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs

# Install readability
RUN npm install @mozilla/readability

# Copy the rest of your application's code
COPY . .

CMD ["python3","utils/publisher.py"]
