from .models import *
#Query all books by a specific author.
qs = Book.objects.filter(author__name="george orwell")
#List all books in a library.
books = Book.objects.all()
books.all() #checker
#Retrieve the librarian for a library.
library = Library.objects.get(name= library_name)
librarian_name = library.librarian.name

