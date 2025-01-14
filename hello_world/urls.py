from django.urls import path
from .views import (
    index,
    home,
    register,
    profile_view,
    edit_profile,
    RoomListingListView,
    create_listing,
    listing_detail,
    message_list,
    send_message,
)

urlpatterns = [
    path('', index, name='index'),  # Homepage
    path('home/', home, name='home'),  # Home view with featured listings
    path('register/', register, name='register'),  # User registration
    path('profile/', profile_view, name='profile'),  # User profile
    path('profile/edit/', edit_profile, name='edit_profile'),  # Edit profile
    path('listings/', RoomListingListView.as_view(), name='listing_list'),  # List of room listings
    path('listings/create/', create_listing, name='create_listing'),  # Create a new room listing
    path('listings/<int:pk>/', listing_detail, name='listing_detail'),  # Room listing detail
    path('messages/', message_list, name='message_list'),  # User messages
    path('messages/send/<int:recipient_id>/', send_message, name='send_message'),  # Send a message
]