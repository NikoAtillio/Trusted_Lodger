from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User, Profile
from .forms import CustomUserCreationForm, ProfileForm

def register(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully!')
            login(request, user)  # Automatically log in the user after registration
            return redirect('home')  # Redirect to home after registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """Handle user login"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')  # Redirect to home after login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')  # Redirect to login page after logout

@login_required
def profile_view(request):
    """Display user profile"""
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    """Edit user profile"""
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def account_settings(request):
    """Display account settings page."""
    return render(request, 'accounts/account_settings.html')

@login_required
def inbox(request):
    """Display inbox page."""
    return render(request, 'accounts/inbox.html')

@login_required
def list_room(request):
    """Display the list room page."""
    return render(request, 'accounts/list_room.html')

@login_required
def manage_listing(request):
    """Display manage listing page."""
    return render(request, 'accounts/manage_listing.html')

@login_required
def room_setup(request):
    """Display room setup page."""
    return render(request, 'accounts/room_setup.html')

@login_required
def saved_searches(request):
    """Display saved searches page."""
    return render(request, 'accounts/saved_searches.html')

@login_required
def profile_setup(request):
    """Display profile setup page."""
    return render(request, 'accounts/profile_setup.html')