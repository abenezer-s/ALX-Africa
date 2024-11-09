from decimal import Decimal
from django.db import models
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from course.models import Category, Course
from django.contrib.auth.models import User

# Create your models here.
class Program(models.Model):
    """
    Prgram consists of one or more courses. 
    """
    owner = models.ForeignKey(User,default=None, on_delete=models.CASCADE, related_name='program_owner')
    name = models.CharField(max_length=150, blank=False, unique=True)
    description = models.TextField(default="default description")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default=None)
    number_of_courses = models.DecimalField(default=0, max_digits=3, decimal_places=0)
    courses = models.ManyToManyField(Course, blank= True, default=None)
    duration = models.IntegerField(default=None)   #estimated number of weeks this program might take to fiinish
    complete_within = models.DecimalField(blank=False, max_digits=2, default=None, decimal_places=0)      #number of weeks a learner has to finish content

    created_at = models.DateField(blank=False)
    def __str__(self) -> str:
        return self.name
    
    @classmethod
    def add_course(cls, program_id, course_id, user):
        """
        Adds course to program with id = program_id.
        """
        try:
            course = Course.objects.get(id=course_id)
        except (Course.DoesNotExist):
            return Response({"error": "Course not found"}, 
                            status=status.HTTP_404_NOT_FOUND)
        try:
            program = Program.objects.get(id=program_id)
        except Program.DoesNotExist:
            return Response({"error": "program not found"}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        if course.owner == program.owner == user:
            
            #check if course has already been added before adding
            contains = Program.objects.filter(Q(courses__id=course_id) & Q(id=program_id)).exists()
            if contains:
                return Response({"error": "Course has already been added"},
                                status=status.HTTP_400_BAD_REQUEST)   
             
            program.courses.add(course)
            num_courses = program.number_of_courses #update number of courses field to reflect chnage
            num_courses += Decimal(1)
            program.number_of_courses = num_courses
            program.save()
            return Response({"message": "course successfully added to program."},
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": "you do not have permission to perform this action"},
                            status=status.HTTP_403_FORBIDDEN)