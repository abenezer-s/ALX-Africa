from .views import list_books, LibraryDetailView
from .views import SignUpView, LibraryLoginView, LibraryLogoutView
from django.urls import path


urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
]
urlpatterns = [
    path('login/', LibraryLoginView.as_view(), name='login'),
    path('logout/', LibraryLogoutView.as_view(), name='logout'),
    path('/register', SignUpView.as_view(), name='register-view'),
    path('/books', list_books, name='book-view'),
    path('/library', LibraryDetailView.as_view, name='library-details')
]