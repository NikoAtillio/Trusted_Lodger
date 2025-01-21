from django.urls import path, include
from . import views

app_name = 'searches'

urlpatterns = [
    path('search/', views.search, name='search'),
    path('results/', views.search_results, name='search_results'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('saved/', views.saved_searches, name='saved_searches'),
    path('saved/save/', views.save_search, name='save_search'),
    path('saved/<int:search_id>/delete/', views.delete_saved_search, name='delete_saved_search'),
    path('saved/<int:search_id>/edit/', views.edit_saved_search, name='edit_saved_search'),
    path('send_message_ajax/<int:pk>/', views.send_message_ajax, name='send_message_ajax'),
    path('saved-ads/', views.saved_ads, name='saved_ads'),
]