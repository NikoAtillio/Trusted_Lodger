from django.contrib import admin
from .models import Property, SavedSearch

admin.site.register(Property)

@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ('user', 'search_name', 'location', 'created_at')
    list_filter = ('created_at', 'property_type', 'room_size')
    search_fields = ('search_name', 'location', 'user__username')