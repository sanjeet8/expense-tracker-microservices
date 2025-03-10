from django.http import JsonResponse
from .tasks import send_notification, send_email_notification


def send_notification_view(request):
    email = request.GET.get("email", "test@example.com")  
    message = request.GET.get("message", "Hello! This is a test notification.")  

    task = send_notification.delay(email, message)  # Pass both arguments

    return JsonResponse({"task_id": task.id, "message": "Notification task started!"})

def send_test_email(request):
    subject = "Test Email from Celery"
    message = "Hello! This is a test email notification."
    recipient_email = "recipient@example.com"

    send_email_notification.delay(subject, message, recipient_email)

    return JsonResponse({"message": "Email task has been queued"})

