from django.test import TestCase
from .models import Book
from rest_framework.test import APIRequestFactory

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Book
from django.contrib.auth.models import User

class BookAPITests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass')

        # Define the book data
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 2021
        }

        # Create a test book
        self.book = Book.objects.create(**self.book_data)
        
        # Define URLs
        self.book_list_url = reverse('book-list')  # Assuming you have a URL name 'book-list'
        self.book_detail_url = reverse('book-detail', kwargs={'pk': self.book.id})  # 'book-detail' URL pattern

    # Test for creating a Book
    def test_create_book(self):
        new_book_data = {
            'title': 'New Book',
            'author': 'New Author',
            'publication_year': 2022
        }
        response = self.client.post(self.book_list_url, new_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.last().title, 'New Book')

    # Test for retrieving a Book
    def test_get_book(self):
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book_data['title'])
        self.assertEqual(response.data['author'], self.book_data['author'])
        self.assertEqual(response.data['publication_year'], self.book_data['publication_year'])

    # Test for updating a Book
    def test_update_book(self):
        updated_data = {
            'title': 'Updated Book',
            'author': 'Updated Author',
            'publication_year': 2020
        }
        response = self.client.put(self.book_detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, updated_data['title'])
        self.assertEqual(self.book.author, updated_data['author'])
        self.assertEqual(self.book.publication_year, updated_data['publication_year'])

    # Test for deleting a Book
    def test_delete_book(self):
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    # Test unauthenticated requests are denied
    def test_unauthenticated_create_book(self):
        self.client.logout()
        new_book_data = {
            'title': 'Unauthenticated Book',
            'author': 'Anonymous Author',
            'publication_year': 2021
        }
        response = self.client.post(self.book_list_url, new_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Assuming you have authentication required

    # Test for authenticated access
    def test_authenticated_access(self):
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test permission scenarios: only authenticated users can update or delete
    def test_update_book_permission(self):
        self.client.logout()  # Simulate an unauthenticated user
        updated_data = {
            'title': 'Unauthorized Update',
            'author': 'Unknown',
            'publication_year': 2023
        }
        response = self.client.put(self.book_detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_permission(self):
        self.client.logout()
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Optional: Test listing all books (public or authenticated)
    def test_list_books(self):
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return the test book created in setUp
