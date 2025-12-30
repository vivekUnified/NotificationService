from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Count
from delivery_gateway.models import NotificationLog

class AdminDashboardStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 1. Status Counts
        status_data = NotificationLog.objects.values('status').annotate(count=Count('status'))
        status_counts = {item['status']: item['count'] for item in status_data}
        
        # 2. Channel Counts
        channel_data = NotificationLog.objects.values('channel').annotate(count=Count('channel'))
        channel_counts = {item['channel']: item['count'] for item in channel_data}
        
        return Response({
            "status_counts": status_counts,
            "channel_counts": channel_counts
        })
