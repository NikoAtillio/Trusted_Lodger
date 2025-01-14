from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Match
from listings.models import RoomListing

@login_required
def create_match(request, room_listing_id):
    """Create a match between a tenant and a landlord for a room listing."""
    room_listing = RoomListing.objects.get(id=room_listing_id)
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