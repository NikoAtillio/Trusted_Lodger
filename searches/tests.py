from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import RoomListing
from searches.models import SavedSearch, SavedAd
from django.utils import timezone

User = get_user_model()

class RoomListingModelTest(TestCase):
    def setUp(self):
        self.landlord = User.objects.create_user(
            email='landlord@example.com',
            password='password',
            user_type='landlord'
        )
        self.listing = RoomListing.objects.create(
            owner=self.landlord,
            title='Test Room',
            description='A nice room',
            size='Single',  # Changed from room_type to size
            price=500,
            location='London',
            search_type='offered',  # Added required field
            available_from=timezone.now().date()  # Added required field
        )

    def test_listing_creation(self):
        self.assertEqual(self.listing.title, 'Test Room')
        self.assertEqual(self.listing.description, 'A nice room')
        self.assertEqual(self.listing.size, 'Single')
        self.assertEqual(self.listing.price, 500)
        self.assertEqual(self.listing.location, 'London')

class RoomListingViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password'
        )
        self.client = Client()
        self.client.login(email='test@example.com', password='password')

    def test_property_detail_view(self):
        """Test the property detail view"""
        listing = RoomListing.objects.create(
            owner=self.user,
            title='Test Room',
            description='A test room',
            size='Single',  # Changed from room_type to size
            price=500,
            location='Test Location',
            search_type='offered',
            available_from=timezone.now().date(),
            # Removed amenities as it's not in the model
            broadband='yes',  # Added instead of amenities
            parking='yes'
        )
        response = self.client.get(reverse('searches:property_detail', kwargs={'pk': listing.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'searches/property_detail.html')

class SearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(email='test@example.com', password='testpass123')

    def test_search_results_view(self):
        """Test the search results view"""
        response = self.client.get(reverse('searches:search_results'))
        self.assertEqual(response.status_code, 200)

