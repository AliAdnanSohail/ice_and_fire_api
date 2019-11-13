from rest_framework import generics, status
import json

from rest_framework.response import Response

from .serializers import BookSerializer
from .models import Book


# Create your views here.


def update_dict(book_dict):
    book_dict.authors = json.loads(book_dict.authors.replace("'", '"'))
    return book_dict


class ListCreateBooksView(generics.ListCreateAPIView):
    serializer_class = BookSerializer

    queryset = Book.objects.all()

    def get_queryset(self):
        books = Book.objects.all()
        return [update_dict(b) for b in books]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = BookSerializer(queryset, many=True)
        return_response = {'data': serializer.data, 'status_code': status.HTTP_200_OK, 'status': 'success'}
        return Response(return_response, status=status.HTTP_200_OK)


class BookDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer

    def get_object(self):
        book = Book.objects.get(pk=self.kwargs['pk'])
        book.authors = json.loads(book.authors.replace("'", '"'))
        return book
