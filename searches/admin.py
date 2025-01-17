from django.contrib import admin
from .models import SavedSearch
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ('user', 'search_name', 'location', 'min_rent', 'max_rent', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'search_name', 'location')
    readonly_fields = ('created_at',)

admin.site.register(SavedSearch, SavedSearchAdmin)