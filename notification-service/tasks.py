from celery import shared_task

@shared_task
def send_notification(email, message):
    print(f"📨 Sending email to {email}: {message}")
    return f"Notification sent to {email}"
