from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, RoomListing, Message

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'gender', 'dob_day', 'dob_month', 'dob_year', 'user_status', 'profile_picture')}),
        ('User type', {'fields': ('user_type',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type'),
        }),
    )
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'get_created_at')
    search_fields = ('user__email', 'location')
    list_filter = ('updated_at',)

    def get_created_at(self, obj):
        return obj.created_at
    get_created_at.short_description = 'Created At'

class RoomListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'location', 'price', 'room_type', 'available', 'created_at')
    list_filter = ('available', 'room_type', 'bills_included', 'created_at')
    search_fields = ('title', 'location', 'postcode')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('owner', 'title', 'description', 'room_type')
        }),
        ('Location & Price', {
            'fields': ('location', 'postcode', 'price')
        }),
        ('Availability', {
            'fields': ('available', 'available_from', 'minimum_stay')
        }),
        ('Additional Details', {
            'fields': ('bills_included',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__email', 'recipient__email', 'subject', 'content')
    readonly_fields = ('created_at',)

# Register models with their respective admin classes
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(RoomListing, RoomListingAdmin)
admin.site.register(Message, MessageAdmin)
