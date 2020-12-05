#!/usr/bin/env bash

exec celery flower --port=5555 --address=0.0.0.0 --broker ${REDIS_URL}