from celery import Celery


def make_celery(app):
    celery = Celery(app.import_name)

    celery.config_from_object(CeleryConfig)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


class CeleryConfig:
    broker_url = 'amqp://pyizcpcy:i8-DLpC9lKVReHWD0--fNDPT_QOJzNCJ@orangutan.rmq.cloudamqp.com/pyizcpcy'
    broker_pool_limit = 1
    broker_connection_timeout = 30
    broker_heartbeat = None
    event_queue_expires = 60  # Will delete all celeryev. queues without consumers after 1 minute.
    worker_prefetch_multiplier = 1  # Disable prefetching, it's causes problems and doesn't help performance
