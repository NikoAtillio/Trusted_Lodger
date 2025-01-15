from django.urls import path
from .views import create_match, match_list, search_matches, view_profiles

app_name = 'matching'

urlpatterns = [
    path('create/<int:room_listing_id>/', create_match, name='create_match'),  # Create a match
    path('list/', match_list, name='match_list'),  # List of matches
    path('search/', search_matches, name='search_matches'),  # Search matches
    path('profiles/', view_profiles, name='view_profiles'),  # View profiles
]