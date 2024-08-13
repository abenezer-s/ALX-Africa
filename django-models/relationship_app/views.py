from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.shortcuts import render
from .models import Book
from .models import Library

# Create your views here.

def  list_books(request):
    qs = Book.objects.all()
    context = {
        'books' : qs
    }

    return render(request, 'relationship_app/list_books.html',context)

class LibraryDetailView(DetailView):
    model =Library
    template_name = 'relationship_app/library_detail.html'


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'relationship_app/registration.html'

class LibraryLoginView(LoginView):
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True

class LibraryLogoutView(LogoutView):
    next_page = 'relationship_app/login'  

