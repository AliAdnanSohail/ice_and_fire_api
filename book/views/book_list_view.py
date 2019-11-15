import json
from django.db.models import Q
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import BookSerializer
from ..models.book import Book


class BookList(APIView):
    def get_query_set(self):
        search_str = self.request.query_params.get('search')
        if search_str:
            queryset = Book.objects.filter(Q(name__icontains=search_str) | Q(country__icontains=search_str) |
                                           Q(publisher__icontains=search_str))
            if search_str.isdigit():
                queryset2 = Book.objects.filter(Q(release_date__year=search_str))
                queryset = queryset.union(queryset2)
        else:
            queryset = Book.objects.all()
        return queryset

    def get(self, request):
        books = self.get_query_set()
        serializer = BookSerializer(books, many=True)
        return_response = {'data': serializer.data, 'status_code': status.HTTP_200_OK, 'status': 'success'}
        return Response(return_response, status=status.HTTP_200_OK)

    def post(self, request):
        book_data = request.data
        serializer = BookSerializer(data=book_data)
        if serializer.is_valid():
            serializer.save()
            return_response = {'data': serializer.data, 'status_code': status.HTTP_201_CREATED, 'status': 'success'}
            return Response(return_response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetail(APIView):
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        book = self.get_object(pk=pk)
        book.authors = json.loads(book.authors.replace("'", '"'))
        serializer = BookSerializer(book)
        return_response = {'data': serializer.data, 'status_code': status.HTTP_200_OK, 'status': 'success'}
        return Response(return_response, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        book = self.get_object(pk=pk)
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
        book = self.get_object(pk=pk)
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
        book = self.get_object(pk=pk)
        book.delete()
        message = 'The book {name} was deleted successfully'.format(name=book.name)
        return_response = {'data': [], 'message': message,
                           'status': 'success', 'status_code': status.HTTP_204_NO_CONTENT}
        return Response(return_response, status=status.HTTP_204_NO_CONTENT)
