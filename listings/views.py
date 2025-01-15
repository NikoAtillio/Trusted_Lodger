from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from .models import RoomListing
from .forms import RoomListingForm, SearchForm

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

# Room Listing Views
class RoomListingListView(ListView):
    """Display and filter room listings"""
    model = RoomListing
    template_name = 'listings/search_results.html'  # Correct path for search results
    context_object_name = 'listings'
    paginate_by = 12

    def get_queryset(self):
        queryset = RoomListing.objects.filter(available=True)
        form = SearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get('location'):
                queryset = queryset.filter(location__icontains=form.cleaned_data['location'])
            if form.cleaned_data.get('min_price'):
                queryset = queryset.filter(price__gte=form.cleaned_data['min_price'])
            if form.cleaned_data.get('max_price'):
                queryset = queryset.filter(price__lte=form.cleaned_data['max_price'])
            if form.cleaned_data.get('room_type'):
                queryset = queryset.filter(room_type=form.cleaned_data['room_type'])
        return queryset