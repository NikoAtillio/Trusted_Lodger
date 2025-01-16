from django.contrib import admin
from .models import SavedSearch

@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ('user', 'search_name', 'location', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('search_name', 'location')
    readonly_fields = ('created_at',)