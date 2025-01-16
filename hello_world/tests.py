from django.test import TestCase
from .models import RoomListing
from accounts.models import User, Profile

class RoomListingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            user_type='lodger'
        )
        self.room_listing = RoomListing.objects.create(
            owner=self.user,
            title='Test Room',
            description='A nice room.',
            room_type='Single',
            price=100.00,
            location='Test Location',
            available=True
        )

    def test_room_listing_creation(self):
        self.assertEqual(self.room_listing.title, 'Test Room')
        self.assertEqual(self.room_listing.price, 100.00)
        self.assertTrue(self.room_listing.available)

# Add more tests as needed for RoomListing and Message models