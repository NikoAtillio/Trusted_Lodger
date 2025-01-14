from django.contrib import admin
from .models import SupportTicket

class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'created_at', 'is_resolved')
    list_filter = ('is_resolved', 'user')
    search_fields = ('subject', 'message')

admin.site.register(SupportTicket, SupportTicketAdmin)