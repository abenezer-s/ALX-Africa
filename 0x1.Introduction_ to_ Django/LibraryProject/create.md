#creats a book titled 1984, authored by George Orwell with publication year 1949

from bookshelf.models import Book
new_book = Book(title='1984', author='George Orwell', publication_year=1949)
new_book.save()

