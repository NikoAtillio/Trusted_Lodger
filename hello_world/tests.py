from django.test import TestCase
from .models import User, Profile, RoomListing

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            user_type='lodger'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.user_type, 'lodger')

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            user_type='lodger'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='This is a test bio.',
            location='Test Location'
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.bio, 'This is a test bio.')
        self.assertEqual(self.profile.location, 'Test Location')

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

# Add more tests as needed for other functionalities