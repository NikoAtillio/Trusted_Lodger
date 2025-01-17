from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Profile, RoomListing, Message

class UserModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            user_type='tenant'
        )

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, get_user_model()))
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.is_tenant)
        self.assertFalse(self.user.is_landlord)

    def test_profile_creation(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertTrue(isinstance(self.user.profile, Profile))

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
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
            username='landlord',
            email='landlord@example.com',
            password='testpass123',
            user_type='landlord'
        )
        self.listing = RoomListing.objects.create(
            owner=self.user,
            title="Test Room",
            description="Test Description",
            price=500.00,
            location="Test Location"
        )

    def test_room_listing_creation(self):
        self.assertEqual(self.listing.title, "Test Room")
        self.assertEqual(self.listing.owner, self.user)