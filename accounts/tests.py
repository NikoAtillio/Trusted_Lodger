from django.test import TestCase
from django.urls import reverse
from .models import User, Profile

class UserRegistrationTest(TestCase):
    def setUp(self):
        self.url = reverse('register')

    def test_registration_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_user_registration(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'password123',
            'password2': 'password123',
            'user_type': 'lodger'
        })
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        self.assertRedirects(response, reverse('home'))

class UserLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.login_url = reverse('login')

    def test_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_user_login(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
        self.assertRedirects(response, reverse('home'))

class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.profile = Profile.objects.create(user=self.user, bio='Test bio', location='Test location')
        self.client.login(username='testuser', password='password123')
        self.profile_url = reverse('profile')

    def test_profile_view(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertContains(response, 'Test bio')

    def test_edit_profile(self):
        edit_url = reverse('edit_profile')
        response = self.client.post(edit_url, {
            'bio': 'Updated bio',
            'location': 'Updated location'
        })
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated bio')
        self.assertEqual(self.profile.location, 'Updated location')
        self.assertRedirects(response, self.profile_url)