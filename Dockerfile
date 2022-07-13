FROM python:3.10

WORKDIR /project

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1

COPY . .


RUN apt-get update && apt-get install --no-install-recommends -y \
    gcc libc-dev libpq-dev &&\
    pip install --no-cache-dir -r requirements.txt &&\
    apt-get install nano