from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import generics, status
from users.models import CourseEnrollment, ProgramEnrollment, UserProfile
from course.models import Course
from program.models import Program
from application.utils import run_checks, complete_enrolling

# Create your models here.
class ProgramApplication(models.Model):
    owner = models.ForeignKey(User,default=None, on_delete=models.CASCADE, related_name='application_program_owner') #program/course owner
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prog_learner')
    motivation_letter = models.TextField(max_length=600, blank=False)
    submitted_at = models.DateField(blank=False)
    program = models.ForeignKey(Program,default=None, null=True, on_delete=models.CASCADE, related_name='application_program')
    status = [
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]
    
    state = models.CharField(max_length=20, default=None, choices=status)

    @classmethod
    def apply(cls, user, program_id, learner_id, serializer, date):
        """
        Method to apply to a program.
        """
        if serializer.is_valid():  
            motivation_letter = serializer.validated_data['motivation_letter']
            try:
                program = Program.objects.get(id=program_id)
            except Program.DoesNotExist:
                return Response({"error":"program not found"},
                                status=status.HTTP_404_NOT_FOUND)
            program_owner = program.owner
            try:
                learner = User.objects.get(id=learner_id)
            except User.DoesNotExist:
                return Response({"error":"User not found"},
                                status=status.HTTP_404_NOT_FOUND)
            #check for double application
            exists = ProgramApplication.objects.filter(learner=learner, program=program)
            if exists:
                return Response({"error":"an application for this course already exists"},
                            status=status.HTTP_400_BAD_REQUEST)
            #check if user is the actual learner
            if user != learner:
                return Response({"error":"can only apply for self."},
                status=status.HTTP_400_BAD_REQUEST)
            ProgramApplication.objects.create(owner=program_owner,
                                                    learner=learner,
                                                    submitted_at=date,
                                                    motivation_letter=motivation_letter,
                                                    program=program,
                                                    state='Pending')
            return Response({"message":"successfully applied to program"},
                                status=status.HTTP_200_OK)
        else:    
            return Response({"error":"invalid serializer"},
                            status=status.HTTP_400_BAD_REQUEST)
         
    @classmethod
    def reject(cls, learner_id, program_id, request):
        #reject application for program
        try:
            learner = User.objects.get(id=learner_id)
            program = Program.objects.get(id=program_id)
            
        except (User.DoesNotExist, Program.DoesNotExist):
            return Response({"error":"no program or learner found by the provided program or program name"},
                            status=status.HTTP_404_NOT_FOUND)
        user = request.user        
        program_owner = program.owner
        if program_owner != user:
            return Response({"error":"You do not have permission to perform this action"},
                            status=status.HTTP_401_UNAUTHORIZED)
        learner_profile = UserProfile.objects.get(user=learner)
        try:
            application = ProgramApplication.objects.get(Q(program=program) & Q(learner=learner))  
        except ProgramApplication.DoesNotExist:
            return Response({"error":"Application for Program not found"},
                            status=status.HTTP_404_NOT_FOUND)
        if application.state == 'accepted':
            #unenroll learner if previous enrolled
            instance = ProgramEnrollment.objects.get(learner=learner_profile, program=program)
            instance.delete()
        elif application.state == 'rejected':
            return Response({"message":"Application to program has already been rejected."},
                        status=status.HTTP_400_BAD_REQUEST)

        application.state = 'rejected'
        application.save()
        return Response({"message":"Application to program rejected succesfully"},
                        status=status.HTTP_200_OK)
    
    @classmethod
    def enroll_in_all(cls, courses, learner_profile, date, deadline=None ):
        """
        Enroll learner in the courses that are part of the program.
        """
        enrolled_count = 0
        for course in courses:
            try:
                CourseEnrollment.objects.get(course=course, learner=learner_profile)
            except CourseEnrollment.DoesNotExist:
                #enroll
                if deadline:
                    CourseEnrollment.objects.create(course=course,
                                                learner=learner_profile,
                                                date_of_enrollment=date,
                                                deadline=deadline)
                    enrolled_count += 1
                else:
                    CourseEnrollment.objects.create(course=course,
                                                learner=learner_profile,
                                                date_of_enrollment=date)
                    enrolled_count += 1
            except CourseEnrollment.MultipleObjectsReturned:
                pass
        if enrolled_count != 0:
            return True
        return False
   
    @classmethod 
    def enroll(cls, learner_profile, program, date):
        """
        Enroll learner in program and possibly in all courses the program contains.
        """
        num_weeks = program.complete_within
        if num_weeks: 
            #enroll with deadlines           
            deadline = date + timedelta(weeks=int(num_weeks))
            ProgramEnrollment.objects.create(learner=learner_profile,
                                            program=program, 
                                            date_of_enrollment=date, 
                                            deadline=deadline)
            #enroll learner in all the courses the program has
            courses = program.courses.all()
            if courses:
                counted = cls.enroll_in_all(courses, learner_profile, date, deadline)
                response = complete_enrolling(counted)
                return response
            
            return Response({"message":"Application to program accepted succesfully"},
                        status=status.HTTP_200_OK)
        else:
            #enroll without deadlines
            ProgramEnrollment.objects.create(learner=learner_profile, 
                                             program=program, 
                                             date_of_enrollment=date)
            courses = program.courses.all()
            if courses:  
                counted = cls.enroll_in_all(courses, learner_profile, date, deadline)
                response = complete_enrolling(counted)
                return response
            
            return Response({"message":"Application to program accepted succesfully"},
                        status=status.HTTP_200_OK)
        
    @classmethod
    def accept(cls, learner_id, program_id, request, date):
        #accept application for program
        user = request.user
        response = run_checks(user, learner_id, program_id, 'program', ProgramApplication)
        if response.data['error']:
            return response 
        
        application = response.data['application']
        program = response.data['object']
        learner = response.data['learner']
        application.state = 'accepted' 
        application.save()
        learner_profile = UserProfile.objects.get(user=learner)
        #enroll learner to program with appropriate deadlines if there are any
        response = cls.enroll(learner_profile, program, date)
        return response

class CourseApplication(models.Model):
    owner = models.ForeignKey(User,default=None, on_delete=models.CASCADE, related_name='application_course_owner') #program/course owner
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_learner')
    motivation_letter = models.TextField(max_length=600, blank=False)
    submitted_at = models.DateField(blank=False)
    course =  models.ForeignKey(Course,default=None, null=True,on_delete=models.CASCADE, related_name='application_course')
    status = [
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]
    state = models.CharField(max_length=20, default=None, choices=status)

    @classmethod
    def validate(cls, user, learner_id, course_id):
        """
        Check existance of instacnes and the existance an application for course.
        """
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error":"course not found"},
                            status=status.HTTP_404_NOT_FOUND)
        try:
            learner = User.objects.get(id=learner_id)
        except User.DoesNotExist:
            return Response({"error":"User not found"},
                            status=status.HTTP_404_NOT_FOUND)
        #check for double application
        exists = CourseApplication.objects.filter(learner=learner, course=course)
        if exists:
            return Response({"error":"an application for this course already exists"},
                        status=status.HTTP_400_BAD_REQUEST)
        #check if user is the actual learner
        if user != learner:
            return Response({"error":"can only apply for self."},
            status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"error":False,
                        "course":course,
                        "learner": learner})
    
    @classmethod
    def apply(cls,  user, course_id, learner_id, serializer, date):
        """
        Method to apply to a course.
        """
        if serializer.is_valid(): 
            motivation_letter = serializer.validated_data['motivation_letter']
            response = cls.validate(user, learner_id, course_id,)
            if response.data['error']:
                return response
            
            course = response.data['course'] 
            learner = response.data['learner']
            course_owner = course.owner
            CourseApplication.objects.create(owner=course_owner, 
                                        learner=learner,
                                        submitted_at=date,
                                        motivation_letter=motivation_letter,
                                        course=course,
                                        state='Pending')
            return Response({"message":"successfully applied to course."},
                            status=status.HTTP_200_OK)
            
        else:    
            return Response({"error":"invalid serializer"},
                            status=status.HTTP_400_BAD_REQUEST)
    
    @classmethod
    def reject(cls, learner_id, course_id, request):
        #reject application for course
        try:
            learner = User.objects.get(id=learner_id)
            course = Course.objects.get(id=course_id)
                      
        except (User.DoesNotExist, Course.DoesNotExist):
            return Response({"error":"no course or learner found by the provided course or learner id"},
                            status=status.HTTP_404_NOT_FOUND)
        learner_profile = UserProfile.objects.get(user=learner)
        course_owner = course.owner
        if course_owner != request.user:
            return Response({"error":"You do not have permission to perform this action"}, 
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            application = CourseApplication.objects.get(Q(course=course) & Q(learner=learner))
        except CourseApplication.DoesNotExist:
            return Response({"error":"Course Application not found"},
                            status=status.HTTP_404_NOT_FOUND)
    
        if application.state == 'accepted':
            #request sent again, remove enrollment for course
            enrollment = CourseEnrollment.objects.get(learner=learner_profile, course=course)
            enrollment.delete()
        elif application.state == 'rejected':
            return Response({"message":"Application to program has already been rejected."},
                        status=status.HTTP_400_BAD_REQUEST)
        application.state = 'rejected'
        application.save()
        return Response({"message":"Application to course rejected succesfully"}, 
                        status=status.HTTP_200_OK)
      
    @classmethod    
    def accept(cls, learner_id, course_id, request, date):
        #accept application for course
        user = request.user
        response = run_checks(user, learner_id, course_id, 'course', CourseApplication)
        if response.data['error']:
            return response
        application = response.data['application']
        course = response.data['object']
        learner = response.data['learner']
        application.state = 'accepted' 
        application.save()
        learner_profile = UserProfile.objects.get(user=learner)
        #enroll learner to course with appropriate deadlines if there are any
    
        num_weeks = course.complete_within
        if num_weeks:
            deadline = date + timedelta(weeks=int(num_weeks))
            CourseEnrollment.objects.create(learner=learner_profile,
                                            course=course,
                                            date_of_enrollment=date, 
                                            deadline=deadline)
        else:
            CourseEnrollment.objects.create(learner=learner_profile,
                                            course=course,
                                            date_of_enrollment=date)
            
        return Response({"message":"Application to course accepted succesfully"},
                        status=status.HTTP_200_OK)