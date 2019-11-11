import logging
import os
from logging.handlers import RotatingFileHandler

from celery import Celery

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
LOG_FORMATTER = '%(asctime)s %(filename)s %(funcName)12s() %(levelname)s %(message)s'


def make_celery(app):
    celery = Celery('tasks')

    celery.config_from_object(CeleryConfig)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


class CeleryConfig:
    broker_url = CELERY_BROKER_URL
    broker_pool_limit = 1
    broker_connection_timeout = 30
    broker_heartbeat = None
    event_queue_expires = 60  # Will delete all celeryev. queues without consumers after 1 minute.
    worker_prefetch_multiplier = 1  # Disable prefetching, it's causes problems and doesn't help performance


def set_logger(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(LOG_FORMATTER))
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
