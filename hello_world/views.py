from django.shortcuts import render
from django.http import HttpResponse

def home_page_view(request):
    return HttpResponse('Hello, World!')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q

from .models import User, Profile, RoomListing, Message
from .forms import (
    CustomUserCreationForm, ProfileForm, RoomListingForm,
    SearchForm, MessageForm
)

# Home View
def home(request):
    """Display homepage with featured listings"""
    listings = RoomListing.objects.filter(available=True)[:6]
    return render(request, 'core/index.html', {
        'listings': listings,
        'search_form': SearchForm()
    })

# Authentication Views
def register(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/account/register.html', {'form': form})

# Profile Views
@login_required
def profile_view(request):
    """Display user profile"""
    profile = Profile.objects.get_or_create(user=request.user)[0]
    return render(request, 'core/profiles/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    """Edit user profile"""
    profile = Profile.objects.get_or_create(user=request.user)[0]
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'core/profiles/edit_profile.html', {'form': form})

# Room Listing Views
class RoomListingListView(ListView):
    """Display and filter room listings"""
    model = RoomListing
    template_name = 'core/listings/search_results.html'
    context_object_name = 'listings'
    paginate_by = 12

    def get_queryset(self):
        queryset = RoomListing.objects.filter(available=True)
        form = SearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get('location'):
                queryset = queryset.filter(
                    location__icontains=form.cleaned_data['location']
                )
            if form.cleaned_data.get('min_price'):
                queryset = queryset.filter(
                    price__gte=form.cleaned_data['min_price']
                )
            if form.cleaned_data.get('max_price'):
                queryset = queryset.filter(
                    price__lte=form.cleaned_data['max_price']
                )
            if form.cleaned_data.get('room_type'):
                queryset = queryset.filter(
                    room_type=form.cleaned_data['room_type']
                )
        return queryset

@login_required
def create_listing(request):
    """Create new room listing"""
    if request.method == 'POST':
        form = RoomListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            messages.success(request, 'Listing created successfully!')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = RoomListingForm()
    return render(request, 'core/listings/create_listing.html', {'form': form})

@login_required
def listing_detail(request, pk):
    """Display room listing details"""
    listing = get_object_or_404(RoomListing, pk=pk)
    return render(request, 'core/listings/listing_detail.html', {'listing': listing})

# Messaging Views
@login_required
def message_list(request):
    """Display user's messages"""
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).order_by('-created_at')
    return render(request, 'core/messages/message_list.html', {'messages': messages})

@login_required
def send_message(request, recipient_id):
    """Send a message to another user"""
    recipient = get_object_or_404(User, pk=recipient_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('message_list')
    else:
        form = MessageForm()
    return render(request, 'core/messages/send_message.html', {
        'form': form,
        'recipient': recipient
    })

# Error Handlers
def custom_404(request, exception):
    return render(request, 'core/errors/404.html', status=404)

def custom_500(request):
    return render(request, 'core/errors/500.html', status=500)