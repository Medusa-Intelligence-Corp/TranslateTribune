FROM selenium/standalone-chrome:latest

WORKDIR /usr/src/app

USER root
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    wget \
    unzip \
    xvfb

RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs

# Create and activate a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip3 install --upgrade --no-cache-dir pip

# Install Python dependencies in the virtual environment
RUN pip3 install --no-cache-dir \
    selenium \
    beautifulsoup4 \
    requests \
    pytz \
    cachetools \
    urlextract \
    langdetect \
    goose3[all] \
    readabilipy \
    Jinja2 \
    bleach \
    func-timeout \
    smartenough \
    boto3 

COPY . .

CMD ["python3", "utils/publisher.py"]
