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
    unzip

# Install Python dependencies
RUN pip3 install --no-cache-dir \
    'selenium==4.1.0'

# Download and extract the bypass-paywalls-chrome-clean-master.zip
RUN wget -O bypass-paywalls-chrome-clean-master.zip "https://gitlab.com/magnolia1234/bypass-paywalls-chrome-clean/-/archive/master/bypass-paywalls-chrome-clean-master.zip" && \
    unzip bypass-paywalls-chrome-clean-master.zip && \
    rm bypass-paywalls-chrome-clean-master.zip

# Copy the rest of your application's code
COPY . .

# Expose port 4444 for Selenium Server
EXPOSE 4444

