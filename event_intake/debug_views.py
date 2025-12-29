from rest_framework.views import APIView
from rest_framework.response import Response
from traffic_control.celery import app

class DebugTasksView(APIView):
    def get(self, request):
        tasks = list(app.tasks.keys())
        print(f"DEBUG: Registered tasks: {tasks}", flush=True)
        return Response(tasks)
