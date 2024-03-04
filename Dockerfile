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
    urlextract \
    validators \
    Jinja2 \
    anthropic 
   

# Copy the rest of your application's code
COPY . .

CMD ["python3","publisher.py"]
