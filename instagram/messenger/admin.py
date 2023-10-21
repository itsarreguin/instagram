from django.contrib import admin

from instagram.messenger.models import Inbox, Message


@admin.register(Inbox)
class InboxModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'uuid']
    list_display_links = ['id', 'uuid']


@admin.register(Message)
class MessageModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'inbox', 'sender', 'receiver', 'created']
    list_display_links = ['id', 'inbox']