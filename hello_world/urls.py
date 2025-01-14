from django.urls import path
from .views import index, base

urlpatterns = [
    path('', index, name='index'),
    path('base/', base, name='base'),
]