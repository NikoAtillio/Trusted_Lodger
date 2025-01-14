from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import SupportTicket

User = get_user_model()

class SupportTicketModelTest(TestCase):
    """Tests for the SupportTicket model"""

    def setUp(self):
        """Create a user and a support ticket for testing"""
        self.user = User.objects.create_user(username='testuser', password='password')
        self.ticket = SupportTicket.objects.create(
            user=self.user,
            subject='Test Ticket',
            message='This is a test ticket.'
        )

    def test_ticket_creation(self):
        """Test that the support ticket is created correctly"""
        self.assertEqual(self.ticket.subject, 'Test Ticket')
        self.assertEqual(self.ticket.message, 'This is a test ticket.')
        self.assertEqual(self.ticket.user, self.user)

class SupportTicketViewTests(TestCase):
    """Tests for the views related to support tickets"""

    def setUp(self):
        """Create a user and log them in for testing views"""
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_create_ticket_view(self):
        """Test the create ticket view"""
        response = self.client.post(reverse('create_ticket'), {
            'subject': 'New Ticket',
            'message': 'Details about the new ticket.',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(SupportTicket.objects.filter(subject='New Ticket').exists())

    def test_ticket_list_view(self):
        """Test the ticket list view"""
        response = self.client.get(reverse('ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'support/ticket_list.html')