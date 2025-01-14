from django.urls import path
from .views import create_match, match_list

urlpatterns = [
    path('create/<int:room_listing_id>/', create_match, name='create_match'),
    path('list/', match_list, name='match_list'),
]