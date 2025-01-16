from django.test import TestCase, Client
from django.urls import reverse

class HelloWorldViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('hello_world:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello_world/index.html')

    def test_about_view(self):
        response = self.client.get(reverse('hello_world:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello_world/about.html')