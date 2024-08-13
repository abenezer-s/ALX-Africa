from .views import list_books, LibraryDetailView
from .views import SignUpView, login_view, LibraryLogoutView
from django.urls import path


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LibraryLogoutView.as_view(), name='logout'),
    path('register/', SignUpView.as_view(), name='register-view'),
    path('books/', list_books, name='book-view'),
    path('library/', LibraryDetailView.as_view, name='library-details')
]