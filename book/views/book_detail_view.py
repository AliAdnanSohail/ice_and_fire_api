import json
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import BookSerializer
from ..models.book import Book


def get_object(pk):
    try:
        return Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404


class BookDetail(APIView):

    def get(self, request, pk):
        book = get_object(pk=pk)
        book.authors = json.loads(book.authors.replace("'", '"'))
        serializer = BookSerializer(book)
        return_response = {'data': serializer.data, 'status_code': status.HTTP_200_OK, 'status': 'success'}
        return Response(return_response, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        book = get_object(pk=pk)
        name = book.name
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            message = 'The book {name} was updated successfully'.format(name=name)
            return_resp = {'data': serializer.data, 'message': message,
                           'status_code': status.HTTP_200_OK, 'status': 'success'}
            return Response(return_resp, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        book = get_object(pk=pk)
        name = book.name
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = 'The book {name} was updated successfully'.format(name=name)
            return_resp = {'data': serializer.data, 'message': message,
                           'status_code': status.HTTP_200_OK, 'status': 'success'}
            return Response(return_resp, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = get_object(pk=pk)
        book.delete()
        message = 'The book {name} was deleted successfully'.format(name=book.name)
        return_response = {'data': [], 'message': message,
                           'status': 'success', 'status_code': status.HTTP_204_NO_CONTENT}
        return Response(return_response, status=status.HTTP_204_NO_CONTENT)
