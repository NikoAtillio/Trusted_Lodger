from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Profile, RoomListing, Message
from datetime import date

class UserModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            user_type='tenant'
        )

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, get_user_model()))
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.is_tenant)
        self.assertFalse(self.user.is_landlord)

    def test_profile_creation(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertTrue(isinstance(self.user.profile, Profile))

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.profile = self.user.profile

    def test_profile_update(self):
        self.profile.bio = "Test bio"
        self.profile.location = "Test location"
        self.profile.save()
        self.assertEqual(self.profile.bio, "Test bio")
        self.assertEqual(self.profile.location, "Test location")

class RoomListingModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='landlord@example.com',
            password='testpass123',
            user_type='landlord'
        )
        self.listing = RoomListing.objects.create(
            owner=self.user,
            title="Test Room",
            description="Test Description",
            price=500.00,
            location="Test Location",
            postcode="SW1A 1AA",  # Valid UK postcode format
            size="Single",
            search_type="offered"
        )

    def test_room_listing_creation(self):
        self.assertEqual(self.listing.title, "Test Room")
        self.assertEqual(self.listing.owner, self.user)

class RoomListingViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='password',
            user_type='landlord'
        )
        self.client = Client()
        self.client.login(email='test@example.com', password='password')

    def test_create_listing_view(self):
        # Test GET request
        response = self.client.get(reverse('accounts:create_listing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/create_listing.html')

        # Test POST request
        test_data = {
            'title': 'Test Room',
            'description': 'A nice room',
            'size': 'Single',  # Changed from room_type to size
            'price': '500.00',
            'location': 'London',
            'postcode': 'SW1A 1AA',  # Valid UK postcode format
            'available_from': date.today(),
            'minimum_term': 1,  # Changed from minimum_stay to minimum_term
            'bills_included': 'yes',  # Changed to match choices
            'search_type': 'offered',
            'deposit': '500.00',
            'furnishings': 'Furnished',
            'parking': 'no',
            'garden': 'no',
            'balcony': 'no',
            'disabled_access': 'no',
            'living_room': 'shared',
            'broadband': 'yes',
            'current_household': 1,
            'total_rooms': 1,
            'ages': '18-30',
            'smoker': 'no',
            'pets': 'no',
            'occupation': 'Professional',
            'gender': 'Any',
            'couples_ok': 'no',
            'smoking_ok': 'no',
            'pets_ok': 'no',
            'occupation_preference': 'Any',
            'references_required': 'yes',
            'min_age': 18,
            'max_age': 99
        }

        response = self.client.post(reverse('accounts:create_listing'), test_data)
        self.assertEqual(response.status_code, 302)  # Redirects after successful creation

        # Verify the listing was created
        self.assertTrue(RoomListing.objects.filter(title='Test Room').exists())
