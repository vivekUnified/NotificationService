from django.urls import path
from .views import EventIntakeView
from .debug_views import DebugTasksView

urlpatterns = [
    path('events/', EventIntakeView.as_view(), name='event-intake'),
    path('debug-tasks/', DebugTasksView.as_view(), name='debug-tasks'),
]
