from django.contrib import admin
from .models import NotificationLog

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'channel', 'status', 'timestamp', 'error_message')
    list_filter = ('status', 'channel', 'timestamp')
    search_fields = ('user_id', 'destination', 'content')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
