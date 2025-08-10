from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book
from django.contrib.auth.models import User


class BookAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.book = Book.objects.create(
            title="Test Book",
            author="John Doe",
            publication_year=2021
        )
        self.list_url = reverse('book-list')  # Adjust to your URL name
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book.pk})

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ✅ Explicitly checking response.data
        self.assertIn('title', response.data[0])
        self.assertEqual(response.data[0]['title'], "Test Book")

    def test_create_book(self):
        self.client.login(username="testuser", password="testpass")
        data = {
            "title": "New Book",
            "author": "Jane Doe",
            "publication_year": 2022
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # ✅ Explicitly checking response.data
        self.assertEqual(response.data['title'], "New Book")

    def test_update_book(self):
        self.client.login(username="testuser", password="testpass")
        data = {
            "title": "Updated Book",
            "author": "John Doe",
            "publication_year": 2023
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ✅ Explicitly checking response.data
        self.assertEqual(response.data['title'], "Updated Book")

    def test_delete_book(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
