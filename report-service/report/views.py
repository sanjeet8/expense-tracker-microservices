from django.http import JsonResponse
from report.tasks import generate_report
from celery.result import AsyncResult
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from report.tasks import generate_report


def get_task_status(request, task_id):
    task = AsyncResult(task_id)
    return JsonResponse({"task_id": task_id, "status": task.status})

class ReportRequestView(APIView):
    def post(self, request):
        task = generate_report.delay()
        return Response({"task_id": task.id, "status": "Report generation started"}, status=status.HTTP_202_ACCEPTED)
