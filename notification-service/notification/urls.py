from django.urls import path
from .views import send_notification_view, send_test_email

urlpatterns = [
    #path("send/", trigger_notification, name="send-notification"),
    path("send-notification/", send_notification_view, name="send-notification"),
    path("send-test-email/", send_test_email, name="send-test-email"),
]
