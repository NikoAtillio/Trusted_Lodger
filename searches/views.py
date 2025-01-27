from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
import json
from .forms import AdvancedSearchForm, SearchFilterForm
from accounts.models import RoomListing, Message
from .models import SavedSearch, SavedAd

def search(request):
    """Initial search page with basic search form"""
    form = AdvancedSearchForm()
    return render(request, 'searches/search.html', {'form': form})

def search_results(request):
    """Handle search results with filters, sorting, and pagination."""
    listings = RoomListing.objects.all()

    # Initialize the form with GET data
    form = SearchFilterForm(request.GET)

    if form.is_valid():
        # Get cleaned data from the form
        location = form.cleaned_data.get('location')
        room_size = form.cleaned_data.get('room_size')
        min_rent = form.cleaned_data.get('min_rent')
        max_rent = form.cleaned_data.get('max_rent')
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
            listings = listings.filter(size=room_size)
        if min_rent:
            listings = listings.filter(price__gte=min_rent)
        if max_rent:
            listings = listings.filter(price__lte=max_rent)
        if property_type:
            listings = listings.filter(property_type__in=property_type)
        if keywords:
            listings = listings.filter(description__icontains=keywords)
        if move_in_date:
            listings = listings.filter(available_from__lte=move_in_date)
        if min_stay:
            listings = listings.filter(minimum_stay__gte=min_stay)

        # Apply sorting
        if sort_by == 'price_low_to_high':
            listings = listings.order_by('price')
        elif sort_by == 'price_high_to_low':
            listings = listings.order_by('-price')
        elif sort_by == 'newest':
            listings = listings.order_by('-created_at')
        elif sort_by == 'location':
            listings = listings.order_by('location')

    # Pagination
    paginator = Paginator(listings, 10)  # 10 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Context for the template
    context = {
        'form': form,  # Pass the form to the template
        'listings': page_obj,
        'total_results': listings.count(),
    }

    return render(request, 'searches/search_results.html', context)


@login_required
def property_detail(request, pk):
    listing = get_object_or_404(RoomListing, pk=pk)
    # Use the helper method instead of direct splitting
    amenities_list = listing.get_amenities_list()

    # Add more context data that might be useful
    context = {
        'property': listing,
        'amenities_list': amenities_list,
        'has_amenities': bool(amenities_list),  # Helper for template conditions
        'similar_properties': RoomListing.objects.filter(
            room_type=listing.room_type
        ).exclude(pk=listing.pk)[:3]  # Add similar properties
    }
    return render(request, 'searches/property_detail.html', context)

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
                room_size=form.cleaned_data.get('room_size', ''),
                property_type=','.join(form.cleaned_data.get('property_type', [])),  # Save as comma-separated string
                amenities=form.cleaned_data.get('keywords', ''),  # Save keywords as amenities
                created_at=form.cleaned_data.get('move_in_date', None)
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

@login_required
def send_message_ajax(request, pk):
    """Handle sending a message via AJAX"""
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            message_content = data.get('message', '').strip()

            # Get the listing
            listing = get_object_or_404(RoomListing, pk=pk)

            if message_content:
                # Create the message
                Message.objects.create(
                    sender=request.user,
                    recipient=listing.owner,
                    subject=f"Message about {listing.title}",
                    content=message_content
                )
                return JsonResponse({
                    'success': True,
                    'message': 'Your message has been sent successfully!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Please enter a message before sending.'
                })

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid request format.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'An error occurred: {str(e)}'
            })

    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    })

@login_required
def saved_ads(request):
    """View saved ads"""
    saved_ads = SavedAd.objects.filter(user=request.user)
    return render(request, 'searches/saved_ads.html', {'saved_ads': saved_ads})