from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import RoomListing
from .models import SavedSearch

User = get_user_model()

class RoomListingModelTest(TestCase):
    def setUp(self):
        self.landlord = User.objects.create_user(
            username='landlord',
            email='landlord@example.com',
            password='password',
            user_type='landlord'
        )
        self.listing = RoomListing.objects.create(
            owner=self.landlord,
            title='Test Room',
            description='A nice room',
            room_type='Single',
            price=500,
            location='London'
        )

    def test_listing_creation(self):
        self.assertEqual(self.listing.title, 'Test Room')
        self.assertEqual(self.listing.description, 'A nice room')
        self.assertEqual(self.listing.room_type, 'Single')
        self.assertEqual(self.listing.price, 500)
        self.assertEqual(self.listing.location, 'London')
        self.assertTrue(self.listing.available)

class RoomListingViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password'
        )
        self.client = Client()
        self.client.login(username='testuser', password='password')

    def test_property_detail_view(self):
        """Test the property detail view"""
        # Create a test listing
        listing = RoomListing.objects.create(
            owner=self.user,
            title='Test Room',
            description='A test room',
            room_type='Single',
            price=500,
            location='Test Location',
            amenities='WiFi, Parking, Pool'
        )
        # Use the correct reverse call with the namespace and pk
        response = self.client.get(reverse('searches:property_detail', kwargs={'pk': listing.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'searches/property_detail.html')

class SearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_search_results_view(self):
        """Test the search results view"""
        response = self.client.get(reverse('searches:search_results'))
        self.assertEqual(response.status_code, 200)

    def test_save_search(self):
        """Test saving a search"""
        response = self.client.post(reverse('searches:save_search'), {
            'search_name': 'Test Search',
            'location': 'Test Location',
            'min_rent': '500',
            'max_rent': '1000'
        })
        self.assertEqual(response.status_code, 302)  # Assuming a redirect after saving
        self.assertEqual(SavedSearch.objects.count(), 1)