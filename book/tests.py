from urllib.parse import urlencode

from rest_framework import status

from .models import Book
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from .serializers import BookSerializer
from django.forms.models import model_to_dict


class BaseViewTest(APITestCase):
    client = APIClient()
    @staticmethod
    def create_book(name, authors, publisher, country, release_date, isbn):
        Book.objects.create(name=name, authors=authors, publisher=publisher,
                            country=country, release_date=release_date, isbn=isbn)

    def setUp(self):
        self.create_book(name='book_name1', authors=['author1', 'author2'], publisher='publisher1',
                         country='country1', release_date='2010-10-10', isbn='isbn1')
        self.create_book(name='book_name2', authors=['author1', 'author2'], publisher='publisher2',
                         country='country2', release_date='2010-10-10', isbn='isbn2')
        self.create_book(name='book_name3', authors=['author1', 'author2'], publisher='publisher3',
                         country='country3', release_date='2010-10-10', isbn='isbn3')


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


class ExternalBookTest(APITestCase):
    def test_get_external_book(self):
        """
        This test is to test our api is returning all books from ice and fire api
        """
        response = self.client.get(reverse('external-book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['status_code'], status.HTTP_200_OK)

        """
        This test is to test our api is returning record from ice and fire api
        on basis of passed parameter name
        """
        book_name = 'A Game of Thrones'
        query_params = urlencode({'name': book_name})
        url = '{url}?{query_params}'.format(url=reverse('external-book-list'), query_params=query_params)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['status_code'], status.HTTP_200_OK)
        self.assertEqual(response.data['data'][0]['name'], book_name)

        """
        This test is to test our api will return valid response if no book is 
        found from ice and fire api
        """
        book_name = 'This should not found'
        query_params = urlencode({'name': book_name})
        url = '{url}?{query_params}'.format(url=reverse('external-book-list'), query_params=query_params)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['status_code'], status.HTTP_200_OK)
        self.assertEqual(response.data['data'], [])
