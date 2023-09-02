from __future__ import unicode_literals , absolute_import

import os

from celery import Celery



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('config.config_celery')

app.autodiscover_tasks()