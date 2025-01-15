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
    faq_support,  # Remember to add this, make sure you have an associated function or view
)

urlpatterns = [
    path('', index, name='index'),  # Homepage
    path('home/', home, name='home'),  # Home view with featured listings
    path('register/', register, name='register'),  # User registration
    path('profile/', profile_view, name='profile'),  # User profile
    path('profile/edit/', edit_profile, name='edit_profile'),  # Edit profile
    path('listings/', RoomListingListView.as_view(), name='listing_list'),  # List of room listings
    path('listings/create/', create_listing, name='create_listing'),  # Create a new room listing
    path('listings/list_room/', create_listing, name='list_room'), # Path for listing a room
    path('listings/<int:pk>/', listing_detail, name='listing_detail'),  # Room listing detail
    path('listings/list_room/', create_listing, name='list_room'),  # Fix for NoReverseMatch error
    path('messages/', message_list, name='message_list'),  # User messages
    path('messages/send/<int:recipient_id>/', send_message, name='send_message'),  # Send a message
    path('support/faq/', faq_support, name='faq_support'),  # FAQ support
    # Add additional paths for future links here
    # path('new_feature/', views.new_feature_view, name='new_feature')  # Example placeholder
]
