from rest_framework import serializers
from .models import Book
import json


class AuthorListField(serializers.ListField):
    child = serializers.CharField()


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorListField()

    class Meta:
        model = Book
        fields = ['id', 'name', 'isbn', 'number_of_pages', 'publisher', 'country', 'release_date', 'authors']

    def to_representation(self, instance):
        data = super(BookSerializer, self).to_representation(instance)
        if type(instance.authors) == str:
            data['authors'] = json.loads(instance.authors.replace("'", '"'))
        return data


