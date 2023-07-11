from django.contrib import admin

from instagram.notifications.models import Notification


@admin.register(Notification)
class NotificationModelAdmin(admin.ModelAdmin):
    pass