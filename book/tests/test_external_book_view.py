from urllib.parse import urlencode
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase


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
