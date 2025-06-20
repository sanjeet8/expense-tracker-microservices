import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notification_service.settings")

app = Celery("notification_service")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: ["notification"])  # ✅ Explicitly add your app name
