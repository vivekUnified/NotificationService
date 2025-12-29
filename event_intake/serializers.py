from rest_framework import serializers

class EventSerializer(serializers.Serializer):
    event_type = serializers.CharField(max_length=100)
    user_id = serializers.CharField(max_length=100)
    payload = serializers.DictField(default=dict)
    timestamp = serializers.DateTimeField(required=False)
    source = serializers.CharField(max_length=100, default='system')
