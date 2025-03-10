from celery import shared_task

@shared_task
def generate_report(user_id):
    print(f"📊 Generating report for user {user_id}")
    return f"Report generated for user {user_id}"
