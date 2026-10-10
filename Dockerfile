FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Europe/Kyiv

RUN apt-get update \
    && apt-get install -y --no-install-recommends cron tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x docker/cron-entrypoint.sh

