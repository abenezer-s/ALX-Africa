from django.urls import path
from .views import *

urlpatterns = [
    path('program/<int:pk>/', ProgramApplicationDetailAPIView.as_view()),
    path('program/', ProgramApplicationListAPIView.as_view()),
    path('program/<int:pk>/update/', ProgramApplicationUpdateAPIView.as_view()),
    path('program/<int:pk>/delete/', ProgramApplicationDestroyAPIView.as_view()),

    path('course/<int:pk>/', CourseApplicationDetailAPIView.as_view()),
    path('course/', CourseApplicationListAPIView.as_view()),
    path('course/<int:pk>/update/', CourseApplicationUpdateAPIView.as_view()),
    path('course/<int:pk>/delete/', CourseApplicationDestroyAPIView.as_view()),

    path('course/<int:course_id>/apply/<int:learner_id>/', ApplyCourse.as_view()),
    path('program/<int:program_id>/apply/<int:learner_id>/', ApplyProgram.as_view()),
    path('course/<int:course_id>/respond/<int:learner_id>/', ApplicationResponseCourse.as_view()),
    path('program/<int:program_id>/respond/<int:learner_id>/', ApplicationResponseProgram.as_view()),

]