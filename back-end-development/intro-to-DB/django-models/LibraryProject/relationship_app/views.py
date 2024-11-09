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