from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileSetupForm, ProfileEditForm, RoomListingForm
from .models import Profile, RoomListing

def login_view(request):
    """Handle user login."""
    next_url = request.POST.get('next', '') or request.GET.get('next', '') or 'hello_world:index'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect(next_url)
        messages.error(request, 'Invalid credentials.')

    return render(request, 'accounts/login.html', {'next': next_url})

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
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Use the default backend
            messages.success(request, 'Registration successful!')
            return redirect('accounts:profile_setup')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_setup(request):
    """Handle initial profile setup."""
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileSetupForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('hello_world:index')
    else:
        form = ProfileSetupForm(instance=profile)

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
            return redirect('accounts:my_profile')  # Redirect to the profile page after editing
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
    listings = request.user.room_listings.all()  # Ensure this matches the related_name in RoomListing
    return render(request, 'accounts/manage_listing.html', {'listings': listings})

@login_required
def create_listing(request):
    """Handle creating a new room listing."""
    if request.method == 'POST':
        form = RoomListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            messages.success(request, 'Room listing created successfully!')
            return redirect('accounts:manage_listing')
    else:
        form = RoomListingForm()
    return render(request, 'accounts/create_listing.html', {'form': form})

@login_required
def my_profile(request):
    """Display the user's main account page."""
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'accounts/my_profile.html', {'profile': profile})

@login_required
def delete_profile(request):
    """Handle profile deletion."""
    if request.method == 'POST':
        profile = get_object_or_404(Profile, user=request.user)
        profile.delete()
        request.user.delete()
        messages.success(request, 'Your profile has been deleted successfully.')
        return redirect('hello_world:index')

    return render(request, 'accounts/delete_profile.html')

def register_view(request):
    """Display the registration form with date options."""
    print("Register view called")  # Debug statement
    days = list(range(1, 32))  # Days from 1 to 31
    months = list(range(1, 13))  # Months from 1 to 12
    years = list(range(1900, 2024))  # Years from 1900 to 2023

    context = {
        'days': days,
        'months': months,
        'years': years,
        'form': UserRegistrationForm(),
    }
    return render(request, 'register.html', context)