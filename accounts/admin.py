from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Message, RoomListing

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_active')
    list_filter = ('user_type', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'created_at')
    search_fields = ('user__username', 'location')
    list_filter = ('created_at',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('subject', 'content', 'sender__username', 'recipient__username')
    date_hierarchy = 'created_at'
    
@admin.register(RoomListing)
class RoomListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'location', 'price', 'room_type', 'available', 'created_at')
    list_filter = ('available', 'room_type', 'bills_included', 'created_at')
    search_fields = ('title', 'description', 'location', 'owner__username')
    date_hierarchy = 'created_at'