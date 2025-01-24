from django.urls import path
from . import views
from .views import my_profile, AccountDetailView

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('inbox/', views.inbox, name='inbox'),
    path('manage/', views.manage_listing, name='manage_listing'),
    path('create-listing/', views.create_listing, name='create_listing'),
    path('profile/', my_profile, name='my_profile'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path('register/profile/', views.register_view, name='register_profile'),  # For profile registration
    path('myaccount/<slug:pk>/', views.AccountDetailView.as_view(), name="myaccount"),
    path('my-viewings/', views.my_viewings, name='my_viewings'),
]
