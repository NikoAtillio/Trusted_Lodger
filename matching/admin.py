from django.contrib import admin
from .models import Match

class MatchAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'landlord', 'room_listing', 'matched_at')
    list_filter = ('tenant', 'landlord')
    search_fields = ('tenant__username', 'landlord__username', 'room_listing__title')

admin.site.register(Match, MatchAdmin)