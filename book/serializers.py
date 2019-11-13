from rest_framework import serializers
from .models import Book


class AuthorListField(serializers.ListField):
    child = serializers.CharField()


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorListField()

    class Meta:
        model = Book
        fields = ['id', 'name', 'isbn', 'number_of_pages', 'publisher', 'country', 'release_date', 'authors']

