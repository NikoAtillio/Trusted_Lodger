from django.urls import path
from .views import (
    register,
    login_view,
    logout_view,
    profile_view,
    edit_profile,
    account_settings,  # New view for account settings
    inbox,             # New view for inbox
    list_room,         # New view for listing a room
    manage_listing,    # New view for managing listings
    room_setup,        # New view for room setup
    saved_searches,    # New view for saved searches
    profile_setup,     # New view for profile setup
)

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),  # User registration
    path('login/', login_view, name='login'),  # User login
    path('logout/', logout_view, name='logout'),  # User logout
    path('profile/', profile_view, name='profile'),  # User profile
    path('profile/edit/', edit_profile, name='edit_profile'),  # Edit user profile
    path('settings/', account_settings, name='account_settings'),  # Account settings
    path('inbox/', inbox, name='inbox'),  # Inbox
    path('list-room/', list_room, name='list_room'),  # List a room
    path('manage-listing/', manage_listing, name='manage_listing'),  # Manage listing
    path('room-setup/', room_setup, name='room_setup'),  # Room setup
    path('saved-searches/', saved_searches, name='saved_searches'),  # Saved searches
    path('profile-setup/', profile_setup, name='profile_setup'),  # Setup profile
]