from django.urls import path
from .views import ReportRequestView, get_task_status

urlpatterns = [
    path('generate-report/', ReportRequestView.as_view(), name='generate_report'),
    path('status/<str:task_id>/', get_task_status, name='get_task_status'),
]
