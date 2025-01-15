from django.urls import path
from .views import (
    RoomListingListView,
    create_listing,
    listing_detail,
    edit_listing,
    delete_listing,
)

app_name = 'listings'

urlpatterns = [
    path('', RoomListingListView.as_view(), name='listing_list'), 
    path('create/', create_listing, name='create_listing'),
    path('<int:pk>/', listing_detail, name='listing_detail'),
    path('<int:pk>/edit/', edit_listing, name='edit_listing'),
    path('<int:pk>/delete/', delete_listing, name='delete_listing'),
    path('search/', RoomListingListView.as_view(), name='search_results'),  # Correctly mapping RoomListingListView
]
