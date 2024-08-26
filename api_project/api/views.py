from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets 
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Book
from .serializers import BookSerializer
# Create your views here.
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes= [IsAuthenticated, IsAdminUser] #Only users that are authenticated and are admin users can access this view

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes= [IsAuthenticated, IsAdminUser] #Only users that are authenticated and are admin users can access this view
