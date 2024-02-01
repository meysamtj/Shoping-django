from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery import signals

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
app = Celery("shoping")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(
    worker_log_format="[%(asctime)s] [%(levelname)s] [%(process)d] [%(task_name)s(%(task_id)s)] %(message)s",
    worker_log_color=True,
)
app.autodiscover_tasks()

