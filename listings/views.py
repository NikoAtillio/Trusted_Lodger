from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RoomListing
from listings.forms import RoomListingForm

@login_required
def create_listing(request):
    """Create a new room listing"""
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
    return render(request, 'listings/create_listing.html', {'form': form})

@login_required
def listing_detail(request, pk):
    """Display room listing details"""
    listing = get_object_or_404(RoomListing, pk=pk)
    return render(request, 'listings/listing_detail.html', {'listing': listing})

@login_required
def listing_list(request):
    """Display a list of room listings"""
    listings = RoomListing.objects.filter(available=True)
    return render(request, 'listings/listing_list.html', {'listings': listings})

@login_required
def edit_listing(request, pk):
    """Edit an existing room listing"""
    listing = get_object_or_404(RoomListing, pk=pk)
    if request.method == 'POST':
        form = RoomListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Listing updated successfully!')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = RoomListingForm(instance=listing)
    return render(request, 'listings/edit_listing.html', {'form': form, 'listing': listing})

@login_required
def delete_listing(request, pk):
    """Delete a room listing"""
    listing = get_object_or_404(RoomListing, pk=pk)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Listing deleted successfully!')
        return redirect('listing_list')
    return render(request, 'listings/delete_listing.html', {'listing': listing})