from django.db import models
import json


class Book(models.Model):
    name = models.CharField(max_length=250, null=False, unique=True)
    isbn = models.CharField(max_length=50)
    authors = models.CharField(max_length=1000)
    number_of_pages = models.PositiveIntegerField(default=0)
    publisher = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    release_date = models.DateField()

    def __str__(self):
        return '{name} By {publisher}'.format(name=self.name, publisher=self.authors)

    def set_authors(self, authors):
        print("---------------In set function--------------", authors)
        self.foo = json.dumps(authors)

    def get_authors(self):
        print("--------------in get function-------------", self.authors)
        return json.loads(self.authors)

