from django.urls import path
from .views import BookList, BookDetail, ExternalBookList


urlpatterns = [
    path('books/', BookList.as_view(), name='books-all'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('external-books/', ExternalBookList.as_view(), name='external-book-list'),
]
