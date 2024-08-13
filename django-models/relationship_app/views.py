from django.views.generic import DetailView
from django.shortcuts import render
from .models import Book, Library

# Create your views here.

def book_view(request):
    qs = Book.objects.all()
    context = {
        'books' : qs
    }

    return render(request, 'relationship_app/list_books.html',context)

class Books_view(DetailView):
    model =Library
    template_name = 'relationship_app/library_detail.html'