from rest_framework import status
from django.urls import reverse

from ..models.book import Book
from ..serializers import BookSerializer
from .base_view import BaseViewTest


class AllBooksTest(BaseViewTest):
    def test_get_all_books(self):
        """
        This test to check endpoint is returning all books
        """
        response = self.client.get(reverse('books-all'))
        expected = Book.objects.all()
        serialized = BookSerializer(expected, many=True)
        self.assertEqual(response.data['data'], serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')

    def test_create_book(self):
        """
        This test to check post request is creating new book
        """
        book = {
            "name": "test_name",
            "isbn": "isbn",
            "number_of_pages": 250,
            "publisher": "test_publisher",
            "country": "test_country",
            "release_date": "2016-02-02",
            "authors": [
                "auth1",
                "auth2"
            ]
        }
        response = self.client.post(reverse('books-all'), book)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status_code'], status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['data']['name'], book['name'])
        self.assertEqual(response.data['data']['authors'], book['authors'])

