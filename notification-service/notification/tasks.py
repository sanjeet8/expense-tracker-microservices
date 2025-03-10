from celery import shared_task
import time
from django.core.mail import send_mail
from django.conf import settings
import smtplib

@shared_task
def send_notification(email, message):
    print(f"Sending notification to user {email}: {message}")
    time.sleep(2)  # Simulating delay
    return f"Notification sent to user {email}"


@shared_task
def test_task():
    print("Test task executed!")
    return "Task Completed!"

@shared_task
def send_email_notification(subject, message, recipient):
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [recipient],
            fail_silently=False,
        )
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")

