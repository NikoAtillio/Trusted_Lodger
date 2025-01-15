from django.urls import path
from .views import create_ticket, ticket_list, about, faq_support

urlpatterns = [
    path('create/', create_ticket, name='create_ticket'),  # Create a new support ticket
    path('list/', ticket_list, name='ticket_list'),  # List of support tickets
    path('about/', about, name='about'),  # About page
    path('faq/', faq_support, name='faq_support'),  # FAQ page
]