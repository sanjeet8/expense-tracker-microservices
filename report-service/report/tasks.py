from celery import shared_task

@shared_task
def generate_report():
    return "Report Generated Successfully!"