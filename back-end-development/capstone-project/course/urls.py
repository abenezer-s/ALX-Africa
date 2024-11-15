from django.urls import path
from .views import *

urlpatterns =[
    path('<int:pk>/', CourseDetailAPIView.as_view()),
    path('create/', CourseCreateAPIView.as_view(), name='creat-course'),
    path('', CourseListAPIView.as_view(), name='courses-api'),
    path('<int:pk>/update/', CourseUpdateAPIView.as_view()),
    path('<int:pk>/delete/', CourseDestroyAPIView.as_view()),
    
]