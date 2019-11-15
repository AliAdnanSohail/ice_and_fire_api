from rest_framework import status
import requests

from rest_framework.response import Response
from rest_framework.views import APIView


def format_external_books(book):
    return {'name': book['name'], 'isbn': book['isbn'], 'authors': book['authors'],
            'number_of_pages': book['numberOfPages'], 'publisher': book['publisher'],
            'country': book['country'], 'release_date': book['released']}


class ExternalBookList(APIView):
    def get(self, request):
        query_params = request.query_params
        base_url = 'https://www.anapioficeandfire.com/api/books'
        res = requests.get(url=base_url, params=query_params)
        status_code, all_books = res.status_code, res.json()
        all_books = [format_external_books(book) for book in all_books]
        return_response = {'data': all_books, 'status_code': status_code, 'status': 'success'}
        return Response(return_response, status=status.HTTP_200_OK)
