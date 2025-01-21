from django.contrib import admin
from .models import SavedAd, SavedSearch

class SavedAdAdmin(admin.ModelAdmin):
    list_display = ('user', 'ad', 'saved_at')
    search_fields = ('user__username', 'ad__title')
    list_filter = ('saved_at',)
    ordering = ('-saved_at',)

class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ('user', 'search_name', 'location', 'created_at')
    search_fields = ('user__username', 'search_name', 'location')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

admin.site.register(SavedAd, SavedAdAdmin)
admin.site.register(SavedSearch, SavedSearchAdmin)
