from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileSetupForm, ProfileEditForm, RoomListingForm
from django.db import transaction, IntegrityError
from datetime import datetime
from .models import Profile, RoomListing, RoomImage
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.views.generic import DetailView
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
import logging
from django.forms.models import model_to_dict
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

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
def edit_ad(request, listing_id):
    listing = get_object_or_404(RoomListing, id=listing_id, owner=request.user)

    if request.method == 'POST':
        form = RoomListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            try:
                listing = form.save(commit=False)
                # If you need to convert available_from to availability
                if 'available_from' in form.cleaned_data:
                    listing.availability = form.cleaned_data['available_from']
                listing.owner = request.user
                listing.save()
                messages.success(request, 'Your ad has been updated successfully!')
                return redirect('accounts:manage_listing')
            except Exception as e:
                messages.error(request, f'Error saving ad: {str(e)}')
                print(f"Error saving listing: {str(e)}")
        else:
            print("Form errors:", form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        # Pre-fill the form with the current listing data
        initial_data = model_to_dict(listing)
        # If you need to convert availability to available_from
        if hasattr(listing, 'availability'):
            initial_data['available_from'] = listing.availability
        form = RoomListingForm(instance=listing, initial=initial_data)

    context = {
        'form': form,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'listing': listing,
    }

    return render(request, 'accounts/edit_ad.html', context)


@login_required
def inbox(request):
    """Display user's messages."""
    messages = request.user.received_messages.all()
    return render(request, 'accounts/inbox.html', {'messages': messages})


@login_required
def create_listing(request):
    if request.method == 'POST':
        form = RoomListingForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Save the RoomListing object
                    listing = form.save(commit=False)
                    listing.owner = request.user
                    listing.save()

                messages.success(request, 'Listing created successfully! Now upload images.')
                return redirect('accounts:upload_images', listing_id=listing.id)  # Redirect to upload images page

            except Exception as e:
                messages.error(request, f'Error creating listing: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RoomListingForm()

    context = {
        'form': form,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    print("Context:", context)  # Debug the context
    return render(request, 'accounts/create_listing.html', context)


@login_required
def upload_images(request, listing_id):
    try:
        # Fetch the RoomListing object
        listing = get_object_or_404(RoomListing, id=listing_id, owner=request.user)

        if request.method == 'POST':
            # Handle POST request: Process uploaded images
            images = request.FILES.getlist('images')
            for image in images:
                RoomImage.objects.create(room_listing=listing, image=image)
                
            # Return a JSON response instead of redirecting
            return JsonResponse({'success': True, 'message': 'Image uploaded successfully!'})

            # Redirect back to the same page to display the uploaded images
            # return redirect('accounts:upload_images', listing_id=listing.id)

        # Handle GET request: Render the upload_images.html template
        images = RoomImage.objects.filter(room_listing=listing)
        return render(request, 'accounts/upload_images.html', {'listing': listing, 'images': images})

    except Exception as e:
        logger.error(f"Error in upload_images view: {str(e)}", exc_info=True)
    
@login_required
def delete_image(request, image_id):
    if request.method == 'POST':
        try:
            image = RoomImage.objects.get(id=image_id)
            # Check if the user owns the image by checking the room_listing owner
            if image.room_listing.owner == request.user:
                image.delete()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
        except RoomImage.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Image not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@login_required
def post_ad(request, listing_id):
    try:
        # Fetch the RoomListing object
        listing = get_object_or_404(RoomListing, id=listing_id, owner=request.user)

        # Mark the listing as live
        listing.is_live = True
        listing.save()

        messages.success(request, 'Your ad is now live!')
        return redirect('accounts:manage_listing')  # Redirect to the manage listings page

    except Exception as e:
        logger.error(f"Error in post_ad view: {str(e)}", exc_info=True)
        messages.error(request, 'An error occurred while posting your ad.')
        return redirect('accounts:upload_images', listing_id=listing_id)


@login_required
def manage_listing(request):
    listings = RoomListing.objects.filter(owner=request.user)
    context = {
        'listings': listings,
    }
    return render(request, 'accounts/manage_listing.html', context)


@login_required
@csrf_exempt
def delete_listing(request, listing_id):
    if request.method == 'POST':
        listing = get_object_or_404(RoomListing, id=listing_id, owner=request.user)
        listing.delete()
        return JsonResponse({'success': True, 'message': 'Listing deleted successfully!'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


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

# My Viewings
def my_viewings(request):
    return render(request, 'path/to/template.html')

