FROM python:3.12-slim

# Instalando alguns pacotes
RUN apt-get update \ 
    && apt-get install -y wget unzip \
    && apt-get clean

ARG CHROME_VERSION="134.0.6998.165"

# Instalando o chrome
RUN wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}-1_amd64.deb \
    && dpkg -i google-chrome-stable_${CHROME_VERSION}-1_amd64.deb || apt-get -fy install \
    && rm google-chrome-stable_${CHROME_VERSION}-1_amd64.deb

# Instalando o chrome-driver
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64 /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver-linux64 \
    && rm chromedriver-linux64.zip

WORKDIR /app

COPY . /app

# Instalando as libs python
RUN pip install -r requirements.txt

ENTRYPOINT []
