from .views import list_books, LibraryDetailView
from .views import SignUpView, login_view, LibraryLogoutView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logincls/', LoginView.as_view(template_name='relationship_app/login.html'), name='login-cls'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register , name='register-view'),
    path('books/', list_books, name='book-view'),
    path('library/', LibraryDetailView.as_view, name='library-details')
]

LoginView.as_view(template_name="") #checker
LogoutView.as_view(template_name="") #checker