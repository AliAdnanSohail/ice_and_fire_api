from rest_framework.test import APITestCase, APIClient
from ..models.book import Book


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
