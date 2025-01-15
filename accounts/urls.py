from django.urls import path
from . import views  # Ensure you use views to maintain consistency

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),  # User registration
    path('login/', views.login_view, name='login'),  # User login
    path('logout/', views.logout_view, name='logout'),  # User logout
    path('profile/', views.profile_view, name='profile'),  # User profile
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Edit user profile
    path('settings/', views.account_settings, name='account_settings'),  # Account settings
    path('inbox/', views.inbox, name='inbox'),  # Inbox
    path('list-room/', views.list_room, name='list_room'),  # List a room
    path('manage-listing/', views.manage_listing, name='manage_listing'),  # Manage listing
    path('room-setup/', views.room_setup, name='room_setup'),  # Room setup
    path('saved-searches/', views.saved_searches, name='saved_searches'),  # Saved searches
    path('profile-setup/', views.profile_setup, name='profile_setup'),  # Setup profile
]
