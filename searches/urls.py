from django.urls import path, include
from . import views

app_name = 'searches'

urlpatterns = [
    path('search/', views.search, name='search'),
    path('results/', views.search_results, name='search_results'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
]