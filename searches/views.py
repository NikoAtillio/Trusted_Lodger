from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
import json
from django.conf import settings
from .forms import AdvancedSearchForm, SearchFilterForm
from accounts.models import RoomListing

def search(request):
    """Initial search page with basic search form"""
    form = AdvancedSearchForm()
    context = {
        'form': form,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,  # Pass the API key
    }
    return render(request, 'searches/search.html', context)

def search_results(request):
    """Handle search results with filters, sorting, and pagination."""
    listings = RoomListing.objects.all()

    # Initialize the form with GET data
    form = SearchFilterForm(request.GET)

    if form.is_valid():
        # Get cleaned data from the form
        location = form.cleaned_data.get('location')
        room_size = form.cleaned_data.get('room_size')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        property_type = form.cleaned_data.get('property_type')
        search_type = form.cleaned_data.get('search_type')
        keywords = form.cleaned_data.get('keywords')
        move_in_date = form.cleaned_data.get('move_in_date')
        min_stay = form.cleaned_data.get('min_stay')
        sort_by = form.cleaned_data.get('sort_by')

        # Apply filters
        if location:
            listings = listings.filter(
                Q(location__icontains=location) |
                Q(postcode__icontains=location)
            )
        if room_size and room_size != 'any':
            listings = listings.filter(size__iexact=room_size)        
        if min_price:
            listings = listings.filter(price__gte=min_price)
        if max_price:
            listings = listings.filter(price__lte=max_price)
        if property_type:
            listings = listings.filter(property_type=property_type)
        if keywords:
            listings = listings.filter(description__icontains=keywords)
        if move_in_date:
            listings = listings.filter(available_from__lte=move_in_date)
        if min_stay:
            listings = listings.filter(minimum_stay__gte=min_stay)
        if search_type:
            listings = listings.filter(search_type=search_type)

        # Apply sorting
        if sort_by == 'price_low_to_high':
            listings = listings.order_by('price')
        elif sort_by == 'price_high_to_low':
            listings = listings.order_by('-price')
        elif sort_by == 'newest':
            listings = listings.order_by('-created_at')
        elif sort_by == 'location':
            listings = listings.order_by('location')

    else:
        print("Invalid form submission:", form.errors)  # Debugging invalid form submissions

    # Pagination
    paginator = Paginator(listings, 10)  # 10 results per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    # Context for the template
    context = {
        'form': form,  # Pass the form to the template
        'listings': page_obj,
        'total_results': paginator.count,  # Use paginator.count for efficiency
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,  # Pass the API key
    }

    return render(request, 'searches/search_results.html', context)


@login_required
def property_detail(request, pk):
    listing = get_object_or_404(RoomListing, pk=pk)
    # Create amenities list from the listing's attributes
    amenities_list = []
    if listing.parking == 'yes':
        amenities_list.append('Parking')
    if listing.garden == 'yes':
        amenities_list.append('Garden')
    if listing.balcony == 'yes':
        amenities_list.append('Balcony')
    if listing.broadband == 'yes':
        amenities_list.append('Broadband')
    if listing.disabled_access == 'yes':
        amenities_list.append('Disabled Access')
    if listing.living_room == 'yes':
        amenities_list.append('Living Room')

    context = {
        'property': listing,
        'amenities_list': amenities_list,
        'has_amenities': bool(amenities_list),
        'similar_properties': RoomListing.objects.filter(
            size=listing.size
        ).exclude(pk=listing.pk)[:3]
    }
    return render(request, 'searches/property_detail.html', context)


