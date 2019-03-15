# default_config.py
from kombu import Queue, Exchange
import os
CELERY_BROKER_URL = 'amqp://pset:pset123456@192.168.0.56:5672//'
CELERY_RESULT_BACKEND = 'amqp://pset:pset123456@192.168.0.56:5672/'
CELERY_QUEUES = (
    Queue('spider_default', Exchange('spider_default'), routing_key='spider_default'),
    Queue('import_task', Exchange('import_task'), routing_key='import_task'),
    Queue('export_task', Exchange('export_task'), routing_key='export_task'),
)

CELERY_DEFAULT_QUEUE = 'spider_default'
CELERY_DEFAULT_EXCHANGE = 'spider_default'
CELERY_DEFAULT_ROUTING_KEY = 'spider_default'

LDAP_PROVIDER_URL = 'LDAP://apolo.storm:389/'
DOC_PATH_ROOT = os.path.join('data', 'doc')

JOBS = [
    {
        'id': 'job1',
        'func': 'spec_server_if:cron_bakup_hmi',
        # 'args': (1, 1),
        'trigger': 'cron',
        'hour': 6,
        'minute': 1
    }
]
