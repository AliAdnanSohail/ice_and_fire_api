from rest_framework import status
from django.urls import reverse
from django.forms.models import model_to_dict

from ..models.book import Book
from .base_view import BaseViewTest


class BookDetailTest(BaseViewTest):
    def test_get_book_detail(self):
        """
        This test is to check book details by passing book id
        """
        book = Book.objects.first()
        response = self.client.get(reverse('book-detail',  kwargs={'pk': book.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['id'], book.id)
        self.assertEqual(response.data['status_code'], status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')

    def test_patch_book_details(self):
        """
        This test is to check patch request for book passed in params
        """
        book = Book.objects.first()
        updated_isbn = "updated_isbn"
        updated_authors = ["updated_auth1", "updated_auth2"]
        book.isbn = updated_isbn
        book.authors = updated_authors
        book = model_to_dict(book)
        response = self.client.patch(reverse('book-detail', kwargs={'pk': book['id']}), book)
        self.assertEqual(response.data['status_code'], status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'The book {name} was updated successfully'.format(name=book['name']))
        self.assertEqual(response.data['data']['isbn'], updated_isbn)
        self.assertEqual(response.data['data']['authors'], updated_authors)

    def test_delete_book_details(self):
        """
        This test is to delete book passed in params
        """
        book = Book.objects.first()
        total_books = Book.objects.count()
        response = self.client.delete(reverse('book-detail', kwargs={'pk': book.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['status_code'], status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'], 'The book {name} was deleted successfully'.format(name=book.name))
        self.assertEqual(Book.objects.count(), total_books-1)

        response = self.client.get(reverse('book-detail', kwargs={'pk': book.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
