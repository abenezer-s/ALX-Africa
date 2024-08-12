from bookshelf.models import Book
#delete book object with id=1 which is 1984

book = Book.objects.get(title='1984')
book.delete()
