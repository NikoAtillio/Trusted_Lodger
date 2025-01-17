from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import AdvancedSearchForm
from accounts.models import RoomListing
from .models import SavedSearch

def search(request):
    """Initial search page with basic search form"""
    form = AdvancedSearchForm()
    return render(request, 'searches/search.html', {'form': form})

def search_results(request):
    """Handle both initial and advanced search"""
    listings = RoomListing.objects.filter(available=True)

    # Get search parameters
    location = request.GET.get('location', '')
    room_type = request.GET.get('room_type', '')

    # Apply filters
    if location:
        listings = listings.filter(
            Q(location__icontains=location) |
            Q(postcode__icontains=location)
        )

    if room_type and room_type != 'any':
        listings = listings.filter(room_type=room_type)

    # Handle advanced search form
    if request.method == 'POST':
        form = AdvancedSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            if data.get('min_rent'):
                listings = listings.filter(price__gte=data['min_rent'])
            if data.get('max_rent'):
                listings = listings.filter(price__lte=data['max_rent'])
            if data.get('bills_included'):
                listings = listings.filter(bills_included=True)
            if data.get('available_from'):
                listings = listings.filter(available_from__lte=data['available_from'])
    else:
        form = AdvancedSearchForm()

    # Pagination
    paginator = Paginator(listings, 12)  # 12 listings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'listings': page_obj,
        'total_results': listings.count(),
        'search_location': location,
        'search_type': room_type,
    }

    return render(request, 'searches/search_results.html', context)

@login_required
def property_detail(request, pk):
    """Display detailed view of a specific property"""
    listing = get_object_or_404(RoomListing, pk=pk)
    return render(request, 'searches/property_detail.html', {'listing': listing})

@login_required
def save_search(request):
    """Save search criteria for alerts"""
    if request.method == 'POST':
        form = AdvancedSearchForm(request.POST)
        if form.is_valid():
            search = SavedSearch(
                user=request.user,
                search_name=request.POST.get('search_name', 'Unnamed Search'),
                location=form.cleaned_data.get('location', ''),
                min_rent=form.cleaned_data.get('min_rent'),
                max_rent=form.cleaned_data.get('max_rent'),
                room_size=form.cleaned_data.get('room_type', '')
            )
            search.save()
            messages.success(request, 'Search saved successfully!')
            return redirect('searches:saved_searches')
    return redirect('searches:search_results')

@login_required
def saved_searches(request):
    """View saved searches"""
    searches = SavedSearch.objects.filter(user=request.user)
    return render(request, 'searches/saved_searches.html', {'saved_searches': searches})

@login_required
def delete_saved_search(request, search_id):
    """Delete a saved search"""
    search = get_object_or_404(SavedSearch, id=search_id, user=request.user)
    search.delete()
    messages.success(request, 'Search deleted successfully!')
    return redirect('searches:saved_searches')

@login_required
def edit_saved_search(request, search_id):
    """Edit a saved search"""
    search = get_object_or_404(SavedSearch, id=search_id, user=request.user)

    if request.method == 'POST':
        form = AdvancedSearchForm(request.POST)
        if form.is_valid():
            # Update the saved search with new values
            search.search_name = request.POST.get('search_name', 'Unnamed Search')
            search.location = form.cleaned_data.get('location', '')
            search.min_rent = form.cleaned_data.get('min_rent')
            search.max_rent = form.cleaned_data.get('max_rent')
            search.room_size = form.cleaned_data.get('room_type', '')
            search.save()

            messages.success(request, 'Search updated successfully!')
            return redirect('searches:saved_searches')
    else:
        # Pre-fill form with existing saved search data
        initial_data = {
            'location': search.location,
            'min_rent': search.min_rent,
            'max_rent': search.max_rent,
            'room_type': search.room_size
        }
        form = AdvancedSearchForm(initial=initial_data)

    return render(request, 'searches/edit_saved_search.html', {
        'form': form,
        'search': search
    })