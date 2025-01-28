from django.contrib import admin
from .models import PropertySearch

@admin.register(PropertySearch)
class PropertySearchAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'search_type', 'search_date')
    list_filter = ('search_type', 'search_date')
    search_fields = ('location', 'user__email')
