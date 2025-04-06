FROM python:latest
LABEL authors="tomato"

ARG API_MODE

WORKDIR app/

COPY requirements_${API_MODE}.txt requirements.txt
COPY gunicorn.conf.py gunicorn.conf.py
RUN pip install -r requirements.txt