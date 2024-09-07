from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Book

class BookAPITests(APITestCase):
    def setUp(self):
        self.book_data = {
            'title': 'Test Book',
            'author': 'Author Name',
            'publication_date': '2023-01-01'
        }
        self.book = Book.objects.create(**self.book_data)
        self.url = reverse('book-detail', kwargs={'pk': self.book.id})

    def test_create_book(self):
        new_book_data = {
            'title': 'New Book',
            'author': 'New Author',
            'publication_date': '2023-01-01'
        }
        response = self.client.post(reverse('book-list'), new_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(id=response.data['id']).title, 'New Book')

    def test_update_book(self):
        updated_data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'publication_date': '2023-01-02'
        }
        response = self.client.patch(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')
        self.assertEqual(self.book.author, 'Updated Author')
        self.assertEqual(str(self.book.publication_date), '2023-01-02')

    def test_delete_book(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)


    def test_permissions(self):
        self.client.logout()  # Ensure the client is not authenticated
        response = self.client.post(reverse('book-list'), self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)