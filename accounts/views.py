from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileSetupForm, ProfileEditForm, RoomListingForm
from .models import Profile, RoomListing
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('hello_world:index')
        messages.error(request, 'Invalid credentials.')
    return render(request, 'accounts/login.html')

def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('hello_world:index')

def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('accounts:profile_setup')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_setup(request):
    """Handle initial profile setup."""
    if request.method == 'POST':
        form = ProfileSetupForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile created successfully!')
            return redirect('hello_world:index')
    else:
        form = ProfileSetupForm()
    return render(request, 'accounts/profile_setup.html', {'form': form})

@login_required
def edit_profile(request):
    """Handle profile editing."""
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:edit_profile')
    else:
        form = ProfileEditForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def inbox(request):
    """Display user's messages."""
    messages = request.user.received_messages.all()
    return render(request, 'accounts/inbox.html', {'messages': messages})

@login_required
def manage_listing(request):
    """Handle property listing management."""
    listings = request.user.listings.all()
    return render(request, 'accounts/manage_listing.html', {'listings': listings})

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = RoomListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect('accounts:manage_listing')
    else:
        form = RoomListingForm()
    return render(request, 'accounts/create_listing.html', {'form': form})
