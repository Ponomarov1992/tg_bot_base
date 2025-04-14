FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/

COPY requirements.txt /usr/src/
RUN pip install --no-cache-dir -r requirements.txt
