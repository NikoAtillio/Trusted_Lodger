from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Match
from listings.models import RoomListing

@login_required
def create_match(request, room_listing_id):
    """Create a match between a tenant and a landlord for a room listing."""
    room_listing = get_object_or_404(RoomListing, id=room_listing_id)
    if request.method == 'POST':
        match = Match.objects.create(
            tenant=request.user,
            landlord=room_listing.owner,
            room_listing=room_listing
        )
        messages.success(request, 'Match created successfully!')
        return redirect('listing_detail', pk=room_listing.id)
    return render(request, 'matching/create_match.html', {'room_listing': room_listing})

@login_required
def match_list(request):
    """Display a list of matches for the logged-in user."""
    matches = Match.objects.filter(tenant=request.user)
    return render(request, 'matching/match_list.html', {'matches': matches})

@login_required
def search_matches(request):
    """Search for matches based on criteria."""
    # Implement search logic here
    return render(request, 'matching/search_matches.html')  # Ensure this path is correct

@login_required
def view_profiles(request):
    """View profiles of landlords or tenants."""
    # Implement profile viewing logic here
    return render(request, 'matching/view_profiles.html')  # Ensure this path is correct