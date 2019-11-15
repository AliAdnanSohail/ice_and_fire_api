from django.urls import path
from .views.external_book_view import ExternalBookList
from .views.book_list_view import BookList, BookDetail

urlpatterns = [
    path('books/', BookList.as_view(), name='books-all'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('external-books/', ExternalBookList.as_view(), name='external-book-list'),
]
