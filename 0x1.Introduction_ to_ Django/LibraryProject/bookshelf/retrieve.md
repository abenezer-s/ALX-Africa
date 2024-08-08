#retrieve book object with id=1 display its title, author and publication year

book = Book.objects.get(title='1984')
title = book.title #1984
author = book.author # George Orwell
publication_year = book.publication_year #1949