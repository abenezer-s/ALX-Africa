from .views import book_view
from django.urls import path
urlpatterns = [
    path('/', book_view, name='book-view'),
]