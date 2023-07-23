FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get -y install \
    libpq-dev gcc \
    libmemcached11 \
    libmemcachedutil2 \
    libmemcached-dev \
    libz-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /client
COPY ../../requirements_client.txt .
RUN python -m pip install --no-cache-dir -r requirements_client.txt
