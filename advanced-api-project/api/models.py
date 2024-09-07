from django.db import models

# Create your models here.
# Author model to store author details
class Author(models.Model):
    name = models.CharField(max_length=100)

# Book model to store book details
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

