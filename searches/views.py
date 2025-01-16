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
    # Initialize queryset
    listings = RoomListing.objects.filter(available=True)

    # Get initial search parameters from session
    initial_location = request.session.get('search_location', '')
    initial_type = request.session.get('search_type', '')

    # Apply initial location filter if exists
    if initial_location:
        listings = listings.filter(
            Q(location__icontains=initial_location) |
            Q(postcode__icontains=initial_location)
        )

    if request.method == 'POST':
        form = AdvancedSearchForm(request.POST)
        if form.is_valid():
            # Apply filters based on form data
            data = form.cleaned_data

            # Price range filter
            if data.get('min_rent'):
                listings = listings.filter(price__gte=data['min_rent'])
            if data.get('max_rent'):
                listings = listings.filter(price__lte=data['max_rent'])

            # Room type filter
            if data.get('room_size') and data['room_size'] != 'any':
                listings = listings.filter(room_type=data['room_size'])

            # Bills included filter
            if data.get('bills_included'):
                listings = listings.filter(bills_included=True)

            # Available from date filter
            if data.get('move_in_date'):
                listings = listings.filter(available_from__lte=data['move_in_date'])

            # Minimum stay filter
            if data.get('min_stay'):
                listings = listings.filter(minimum_stay__gte=int(data['min_stay']))
    else:
        form = AdvancedSearchForm()

    # Add pagination
    paginator = Paginator(listings, 10)  # Show 10 listings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
        'listings': page_obj,
        'initial_location': initial_location,
        'initial_type': initial_type,
        'total_results': listings.count(),
    }

    return render(request, 'searches/search_results.html', context)

@login_required  # Add this if you want to restrict access to logged-in users only
def property_detail(request, pk):
    """Display detailed view of a specific property"""
    property = get_object_or_404(RoomListing, pk=pk)
    return render(request, 'searches/property_detail.html', {'property': property})

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
                property_type=','.join(form.cleaned_data.get('property_type', [])),
                room_size=form.cleaned_data.get('room_size', '')
            )
            search.save()
            messages.success(request, 'Search criteria saved successfully!')
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
    messages.success(request, 'Saved search deleted successfully!')
    return redirect('searches:saved_searches')

@login_required
def edit_saved_search(request, search_id):
    """Edit a saved search"""
    search = get_object_or_404(SavedSearch, id=search_id, user=request.user)
    if request.method == 'POST':
        form = AdvancedSearchForm(request.POST)
        if form.is_valid():
            search.search_name = request.POST.get('search_name', 'Unnamed Search')
            search.location = form.cleaned_data.get('location', '')
            search.min_rent = form.cleaned_data.get('min_rent')
            search.max_rent = form.cleaned_data.get('max_rent')
            search.property_type = ','.join(form.cleaned_data.get('property_type', []))
            search.room_size = form.cleaned_data.get('room_size', '')
            search.save()
            messages.success(request, 'Saved search updated successfully!')
            return redirect('searches:saved_searches')
    else:
        initial_data = {
            'location': search.location,
            'min_rent': search.min_rent,
            'max_rent': search.max_rent,
            'property_type': search.property_type.split(',') if search.property_type else [],
            'room_size': search.room_size
        }
        form = AdvancedSearchForm(initial=initial_data)

    return render(request, 'searches/edit_saved_search.html', {
        'form': form,
        'search': search
    })