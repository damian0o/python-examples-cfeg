FROM python:3-slim

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

WORKDIR /app

ENV REDIS_URL=redis://redis:6379//

ENTRYPOINT ["/app/entrypoint.sh"]
