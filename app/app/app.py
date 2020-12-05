import os
from flask import Flask
import redis
import logging
import uuid
from celery import Celery, group
from celery.schedules import crontab
from time import sleep
from prometheus_flask_exporter import PrometheusMetrics

from app.config import Config

os.environ.setdefault('DEBUG_METRICS', 'true')

logging.basicConfig(level=logging.DEBUG)

config = Config("/app/config.yml")

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = config.celery_backend
app.config['CELERY_RESULT_BACKEND'] = config.celery_backend

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

metrics = PrometheusMetrics(app)

metrics.info('app_info', 'Application info', version='0.1.0')

by_path_counter = metrics.counter(
    'by_path_counter', 'Request count by request paths',
    labels={'path': lambda: request.path}
)

cache = redis.Redis(host='redis', port=6379, db=2)

@celery.task()
def do_sub_work(name):
    sleep(2)
    return f"name: {name}"

def generate_tasks(count, id):
    for no in range(1, 3):
        yield do_sub_work.s(f'{count} {id} - {no}')

@celery.task()
def do_work(count):
    results = group(generate_tasks(count, str(uuid.uuid4())))()
    logging.info(str(results))
    sleep(5)
    return f"Hello {count}"

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    task = do_work.apply_async(args=[count])
    return 'Hello World! I have been seen {} times OH YEE 5.\n'.format(count)
