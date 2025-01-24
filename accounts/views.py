from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileSetupForm, ProfileEditForm, RoomListingForm
from django.db import transaction, IntegrityError
from datetime import datetime
from .models import Profile, RoomListing
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.views.generic import DetailView
from django.contrib.auth.forms import PasswordChangeForm

def login_view(request):
    """Handle user login."""
    next_url = request.POST.get('next', '') or request.GET.get('next', '') or 'hello_world:index'

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password.')
            print(f"Login failed for email: {email}")  # Debug print

    return render(request, 'accounts/login.html', {'next': next_url})
def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('hello_world:index')

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create and save the user
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password1'])
                    user.save()

                    # The profile is automatically created by the signal
                    # Just update the profile with form data
                    user.profile.gender = form.cleaned_data['gender']
                    user.profile.dob_day = form.cleaned_data['dob_day']
                    user.profile.dob_month = form.cleaned_data['dob_month']
                    user.profile.dob_year = form.cleaned_data['dob_year']

                    # Handle optional fields
                    if form.cleaned_data.get('occupation'):
                        user.profile.occupation = form.cleaned_data['occupation']
                    if form.cleaned_data.get('availability'):
                        user.profile.availability = form.cleaned_data['availability']
                    if form.cleaned_data.get('budget'):
                        user.profile.budget = form.cleaned_data['budget']

                    # Handle profile picture if provided
                    if 'profile_picture' in request.FILES:
                        user.profile.profile_picture = request.FILES['profile_picture']

                    user.profile.save()

                    # Log the user in
                    user = authenticate(
                        request,
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password1']
                    )
                    if user is not None:
                        login(request, user)
                        messages.success(request, 'Registration successful!')
                        return redirect('accounts:edit_profile')
                    else:
                        messages.error(request, 'Authentication failed after registration.')

            except Exception as e:
                print(f"Registration error: {str(e)}")
                messages.error(request, 'Registration failed. Please try again.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {
        'form': form,
        'days': range(1, 32),
        'months': range(1, 13),
        'years': range(datetime.now().year - 100, datetime.now().year - 17)
    })
    """
    # Original register function kept for reference
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('accounts:profile_setup')
        else:
            # Errors will automatically be bound to their respective fields
            print("Form errors:", form.errors)
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
        'days': range(1, 32),
        'months': range(1, 13),
        'years': range(datetime.now().year - 100, datetime.now().year - 17),
    }
    return render(request, 'accounts/register.html', context)
    """


@login_required
def edit_profile(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        print('POST:', request.POST)
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(request, 'Profile updated successfully!')
                    return redirect('accounts:my_profile')
            except Exception as e:
                messages.error(request, f'Error updating profile: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
            print("Form errors:", form.errors)  # For debugging
    else:
        form = ProfileEditForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
        'user': user,
        'days': range(1, 32),
        'months': range(1, 13),
        'years': range(datetime.now().year - 100, datetime.now().year - 17)
    }

    return render(request, 'accounts/edit_profile.html', context)

@login_required
def inbox(request):
    """Display user's messages."""
    messages = request.user.received_messages.all()
    return render(request, 'accounts/inbox.html', {'messages': messages})

@login_required
def manage_listing(request):
    """Handle property listing management."""
    listings = request.user.room_listings.all()
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
    years = list(range(1900, 2025))  # Years from 1900 to 2023

    context = {
        'days': days,
        'months': months,
        'years': years,
        'form': UserRegistrationForm(),
    }
    return render(request, 'accounts/register.html', context)


# https://ccbv.co.uk/projects/Django/5.0/django.views.generic.detail/DetailView/

class AccountDetailView(DetailView):
    model = Profile
    template_name = 'accounts/account.html'
    context_object_name = 'profile'

