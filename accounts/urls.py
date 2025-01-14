from django.urls import path
from .views import (
    register,
    login_view,
    logout_view,
    profile_view,
    edit_profile,
)

urlpatterns = [
    path('register/', register, name='register'),  # User registration
    path('login/', login_view, name='login'),  # User login
    path('logout/', logout_view, name='logout'),  # User logout
    path('profile/', profile_view, name='profile'),  # User profile
    path('profile/edit/', edit_profile, name='edit_profile'),  # Edit user profile
]