from .views import list_books, LibraryDetailView
from .views import SignUpView, login_view, LibraryLogoutView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views, librarian_view, member_view, admin_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logincls/', LoginView.as_view(template_name='relationship_app/login.html'), name='login-cls'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register , name='register-view'),
    path('books/', list_books, name='book-view'),
    path('library/', LibraryDetailView.as_view, name='library-details'),
    
    path('admin/', admin_view.admin_view, name='admin-view'),
    path('librarian/', librarian_view.librarian_view, name='librarian-view'),
    path('member/', member_view.member_view, name='member-view'),

    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
]
