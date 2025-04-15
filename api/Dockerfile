FROM python:latest
LABEL authors="tomato"

ARG API_MODE
#This env is now re-used and set again within the container
ENV API_MODE=$API_MODE

WORKDIR app/

COPY requirements_${API_MODE}.txt requirements.txt
COPY gunicorn.conf.py gunicorn.conf.py
RUN pip install -r requirements.txt
