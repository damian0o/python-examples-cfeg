from dataclasses import dataclass
from datetime import datetime, timedelta
from urllib.parse import urlsplit, urlencode, urlunsplit, parse_qsl

from elasticsearch_dsl import connections
from pyhocon import ConfigFactory

class Config:
    def __init__(self, config_path):
        config = ConfigFactory.parse_file(config_path)
        self.celery_backend = config['celery-backend']
