from django.contrib import admin
from .models import UserPreference

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'channel', 'enabled', 'destination')
    list_filter = ('channel', 'enabled')
    search_fields = ('user_id', 'destination')
    list_editable = ('enabled',)
