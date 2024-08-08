#retrieve book object with id=1 display its title, author and publication year

book = Book.objects.get(id=1)
title = book.title
author = book.author
publication_year = book.publication_year