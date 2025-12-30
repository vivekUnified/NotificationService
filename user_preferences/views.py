from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import UserPreference
from .serializers import UserPreferenceSerializer

class UserPreferenceViewSet(viewsets.ModelViewSet):
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user_id', 'channel', 'enabled']
    search_fields = ['user_id', 'destination']
