# Implementing Basic OOP for a Library Management System
class Book:

        def __init__(self, title, author):
            self.title = title
            self.author = author
            self._is_checked_out = False
        
        def get_title(self):
             return self.title
        
        def get_author(self):
            return self.author
        
        def set_status(self, status):
            self._is_checked_out = status

        def get_status(self):
            return self._is_checked_out 
        def __str__(self):
             return f"{self.title} by {self.author}"

class Library:
      
    def __init__(self) -> None:
            self._books = []

    def add_book(self, book):
      self._books.append(book)

    def check_out_book(self, title):
         for book in self._books:
              if book.get_title() == title:
                   book.set_status(True)

    def return_book(self, title):
         for book in self._books:
              if book.get_title() == title:
                   book.set_status(False)

    def list_available_books(self):
         for book in self._books:
              if book._is_checked_out != True:
                   print(book)


      
      