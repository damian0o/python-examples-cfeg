FROM python:3.7-alpine

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app /app

ENV FLASK_APP /app/app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
EXPOSE 5000

WORKDIR /
