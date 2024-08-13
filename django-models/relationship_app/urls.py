from .views import list_books, LibraryDetailView
from django.urls import path
urlpatterns = [
    path('/books', list_books, name='book-view'),
    path('/library', LibraryDetailView.as_view, name='library-details')
]