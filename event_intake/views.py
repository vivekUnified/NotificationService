from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EventSerializer
from .tasks import publish_event
import logging

logger = logging.getLogger(__name__)

class EventIntakeView(APIView):
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event_data = serializer.validated_data
            # Async publish to queue
            publish_event.delay(event_data)
            logger.info(f"Event received and queued: {event_data['event_type']}")
            return Response({"status": "accepted", "message": "Event queued for processing"}, status=status.HTTP_202_ACCEPTED)
        else:
            logger.warning(f"Invalid event payload: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
