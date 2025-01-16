from django.contrib import admin
from .models import RoomListing, Message  # Only import the models we have

@admin.register(RoomListing)
class RoomListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'location', 'price', 'available')
    list_filter = ('available', 'room_type', 'created_at')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'created_at'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('subject', 'content', 'sender__username', 'recipient__username')
    date_hierarchy = 'created_at'