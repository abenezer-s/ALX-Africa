from .models import *
#Query all books by a specific author.
Author.objects.get(name=author_name)
objects.filter(author=author)
qs = Book.objects.filter(author_name=author_name)
#List all books in a library.
books = Book.objects.all()
books.all() #checker
#Retrieve the librarian for a library.
library = Library.objects.get(name=library_name)
librarian_name = library.librarian.name
Librarian.objects.get(library=)

