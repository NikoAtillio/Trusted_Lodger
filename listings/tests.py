from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import RoomListing

User = get_user_model()

class RoomListingModelTest(TestCase):
    """Tests for the RoomListing model"""

    def setUp(self):
        """Create a user and a room listing for testing"""
        self.user = User.objects.create_user(username='testuser', password='password')
        self.listing = RoomListing.objects.create(
            title='Test Room',
            description='A room for testing purposes.',
            owner=self.user,
            available=True
        )

    def test_listing_creation(self):
        """Test that the room listing is created correctly"""
        self.assertEqual(self.listing.title, 'Test Room')
        self.assertEqual(self.listing.description, 'A room for testing purposes.')
        self.assertEqual(self.listing.owner, self.user)
        self.assertTrue(self.listing.available)

class RoomListingViewTests(TestCase):
    """Tests for the views related to room listings"""

    def setUp(self):
        """Create a user and log them in for testing views"""
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_listing_list_view(self):
        """Test the listing list view"""
        response = self.client.get(reverse('listing_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/listing_list.html')

    def test_create_listing_view(self):
        """Test the create listing view"""
        response = self.client.post(reverse('create_listing'), {
            'title': 'New Room',
            'description': 'A new room for testing.',
            'available': True,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(RoomListing.objects.filter(title='New Room').exists())

    def test_listing_detail_view(self):
        """Test the listing detail view"""
        response = self.client.get(reverse('listing_detail', args=[self.listing.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listings/listing_detail.html')

    def test_edit_listing_view(self):
        """Test the edit listing view"""
        response = self.client.post(reverse('edit_listing', args=[self.listing.pk]), {
            'title': 'Updated Room',
            'description': 'An updated room description.',
            'available': True,
        })
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.title, 'Updated Room')
        self.assertEqual(response.status_code, 302)  # Redirect after successful edit

    def test_delete_listing_view(self):
        """Test the delete listing view"""
        response = self.client.post(reverse('delete_listing', args=[self.listing.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(RoomListing.objects.filter(pk=self.listing.pk).exists())