from django.contrib import admin
from .models import RoomListing

class RoomListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'available', 'created_at')
    list_filter = ('available', 'owner')
    search_fields = ('title', 'description')

admin.site.register(RoomListing, RoomListingAdmin)