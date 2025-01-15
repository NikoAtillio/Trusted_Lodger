from django.urls import path
from .views import (
    RoomListingListView,
    create_listing,
    listing_detail,
    edit_listing,
)

app_name = 'listings'

urlpatterns = [
    path('', RoomListingListView.as_view(), name='listing_list'),  # List of room listings
    path('create/', create_listing, name='create_listing'),  # Create a new room listing
    path('<int:pk>/', listing_detail, name='listing_detail'),  # Room listing detail
    path('<int:pk>/edit/', edit_listing, name='edit_listing'),  # Edit room listing
]