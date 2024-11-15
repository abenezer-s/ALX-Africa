from django.shortcuts import render
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics, status, filters
from rest_framework.response import Response
from permissions import IsContentCreator
from .models import *
from .serializers import *
from program.models import Program
from decimal import Decimal

class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerialzer
    permission_classes = [IsAuthenticated]
    

class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.all() 
    serializer_class = CourseSerialzer
    permission_classes = [IsAuthenticated, IsContentCreator]

    def perform_create(self, serializer):
        date = datetime.now()
        serializer.save(owner=self.request.user, created_at=date)

class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerialzer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['category__name', 'duration']
    search_fields = ['name', 'owner__username']

class CourseUpdateAPIView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerialzer
    permission_classes = [IsContentCreator]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.owner != request.user:
            raise PermissionDenied("You do not have permission to edit this course.")
        return super().update(request, *args, **kwargs)

class CourseDestroyAPIView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerialzer
    permission_classes = [IsContentCreator]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.owner != request.user:
            raise PermissionDenied("You do not have permission to delete this course.")
        
        programs = Program.objects.filter(courses__name=instance.name)
        if programs:
            for program in programs:
            #adjust course count for each program course belongs to
                num_courses= program.number_of_courses          #update number of modules field to reflect chnage
                num_courses -= Decimal(1)
                program.number_of_courses = num_courses
                program.save()

        instance.delete()
        return Response({"message": "Course deleted successfully."}, 
                        status=status.HTTP_200_OK)

#categories
class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerialzer
    permission_classes = [IsAuthenticated]

class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerialzer
    permission_classes = [IsAuthenticatedOrReadOnly, IsContentCreator] 

    def perform_create(self, serializer):
        date = datetime.now()
        serializer.save(owner=self.request.user)

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerialzer
    permission_classes = [IsAuthenticated]

class CategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerialzer
    permission_classes = [IsContentCreator]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.owner != request.user:
            raise PermissionDenied("You do not have permission to delete this category.")
        return super().update(request, *args, **kwargs)

class CategoryDestroyAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerialzer
    permission_classes = [IsContentCreator]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
    
        # Check ownership
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this category.")
        
        instance.delete()
        return Response({"message": "Category deleted successfully."}, 
                        status=status.HTTP_200_OK)
