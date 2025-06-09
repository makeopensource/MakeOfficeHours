FROM python:latest
LABEL authors="tomato"

WORKDIR app/

COPY requirements.txt .
COPY gunicorn.conf.py gunicorn.conf.py
RUN pip install -r requirements.txt
