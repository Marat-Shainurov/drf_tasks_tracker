FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY reqiurements.txt .

RUN pip install requirements.txt

COPY . .