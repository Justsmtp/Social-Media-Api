from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'actor', 'verb', 'recipient', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
