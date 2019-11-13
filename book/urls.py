from django.urls import path
from .views import ListCreateBooksView, BookDetailsView


urlpatterns = [
    path('books/', ListCreateBooksView.as_view(), name='book-all'),
    path('books/<int:pk>/', BookDetailsView.as_view(), name='book-detail')
]
