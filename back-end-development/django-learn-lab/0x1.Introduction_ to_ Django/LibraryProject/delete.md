#delete book object with id=1 which is 1984
book = Book.objects.get(id=1)
book.delete()
