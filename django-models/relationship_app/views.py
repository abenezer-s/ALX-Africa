from django.shortcuts import render
from .models import Book

# Create your views here.
def book_view(request):
    qs = Book.objects.all()
    context = {
        'querset' = qs
    }

    return render(request, 'list_books.html',context)