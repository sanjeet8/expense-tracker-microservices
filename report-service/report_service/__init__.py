from .celery import app as celery_app
import report.tasks 
__all__ = ('celery_app',)
