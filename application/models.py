from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import generics, status
from users.models import CourseEnrollment, ProgramEnrollment, UserProfile
from course.models import Course
from program.models import Program

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
    def apply(cls, program_id, learner_id, serializer, date):
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
    def enroll_in_all(cls, courses, learner_profile, date, deadline=None ):
            #enroll learner in the courses quesryset if they hav not been enrolled already
            
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
                    else:
                        
                        CourseEnrollment.objects.create(course=course,
                                                    learner=learner_profile,
                                                    date_of_enrollment=date)
            return
    
    @classmethod
    def reject(cls, learner_id, program_id, request):
        #reject application for program
        try:
            learner_obj = User.objects.get(id=learner_id)
            program = Program.objects.get(id=program_id)
            
        except (User.DoesNotExist, Program.DoesNotExist):
            return Response({"error":"no program or learner found by the provided program or program name"},
                            status=status.HTTP_404_NOT_FOUND)
        
        program_owner = program.owner
        if program_owner != request.user:
            return Response({"error":"You do not have permission to perform this action"},
                            status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            application = ProgramApplication.objects.get(Q(program=program) & Q(learner=learner_obj))  
        except ProgramApplication.DoesNotExist:
            return Response({"error":"Application for Program not found"},
                            status=status.HTTP_404_NOT_FOUND)
        
        application.state = 'rejected'
        application.save()
        return Response({"message":"Application to program rejected succesfully"},
                        status=status.HTTP_200_OK)

    @classmethod
    def accept(cls, learner_id, program_id, request, date):
        #accept application for program
        try:
            learner = User.objects.get(id=learner_id)   
            program = Program.objects.get(id=program_id)       

        except (User.DoesNotExist, Program.DoesNotExist):
            return Response({"error":"no program or learner found by the provided program or program name"},
                            status=status.HTTP_404_NOT_FOUND)
        
        learner_profile = UserProfile.objects.get(user=learner)
        program_owner = program.owner
        if program_owner != request.user:
                return Response({"error":"You do not have permission to perform this action"},
                                status=status.HTTP_401_UNAUTHORIZED)
        try:
            application = ProgramApplication.objects.get(Q(program=program) & Q(learner=learner))
            
        except ProgramApplication.DoesNotExist:
            return Response({"error":"Application not found"},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            state = application.state 
            if state == 'accepted':
                return Response({"error":"Application has already been accepted"},
                        status=status.HTTP_400_BAD_REQUEST)
            
            application.state = 'accepted' 
            application.save()
        
        #enroll learner to program with appropriate deadlines if there are any
        num_weeks = program.complete_within
        if num_weeks:
            
            deadline = date + timedelta(weeks=int(num_weeks))
            ProgramEnrollment.objects.create(learner=learner_profile,
                                            program=program, 
                                            date_of_enrollment=date, 
                                            deadline=deadline)
            
            #enroll learner in all the courses the program has
            courses = program.courses.all()
            if courses:
                cls.enroll_in_all(courses, learner_profile, date, deadline)
                message = 'Application to program accepted succesfully. Leaner enrolled in program and courses within the program'
                
                return Response({"message": message},
                                status=status.HTTP_200_OK)
            
            return Response({"message":"Application to program accepted succesfully"},
                        status=status.HTTP_200_OK)

        else:
            #with out deadlines
            
            ProgramEnrollment.objects.create(learner=learner_profile, 
                                             program=program, 
                                             date_of_enrollment=date)
            courses = program.courses.all()
            if courses:
                
                cls.enroll_in_all(courses, learner_profile, date)
                message = 'Application to program accepted succesfully. Learner enrolled in the program and courses within the program'
                
                return Response({"message": message},
                        status=status.HTTP_200_OK)
            
        return Response({"message":"Application to program accepted succesfully"},
                        status=status.HTTP_200_OK)


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
    def apply(cls, course_id, learner_id, user, serializer, date):
        """
        Method to apply to a course.
        """
        if serializer.is_valid():
            
            motivation_letter = serializer.validated_data['motivation_letter']

            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return Response({"error":"course not found"},
                                status=status.HTTP_404_NOT_FOUND)
            course_owner = course.owner
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
            if user == learner:
                CourseApplication.objects.create(owner=course_owner, 
                                            learner=learner,
                                            submitted_at=date,
                                            motivation_letter=motivation_letter,
                                            course=course,
                                            state='Pending')
            else:
                return Response({"error":"can only apply for self."},
                status=status.HTTP_400_BAD_REQUEST)    
            
            return Response({"message":"successfully applied to course."},
                            status=status.HTTP_200_OK)
            
        else:    
            return Response({"error":"invalid serializer"},
                            status=status.HTTP_400_BAD_REQUEST)
    
    @classmethod
    def reject(cls, learner_id, course_id, request):
        #reject application for course
        try:
            learner_obj = User.objects.get(id=learner_id)
            course = Course.objects.get(id=course_id)
                      
        except (User.DoesNotExist, Course.DoesNotExist):
            return Response({"error":"no course or learner found by the provided course or learner id"},
                            status=status.HTTP_404_NOT_FOUND)

        course_owner = course.owner
        if course_owner != request.user:
            return Response({"error":"You do not have permission to perform this action"}, 
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            application = CourseApplication.objects.get(Q(course=course) & Q(learner=learner_obj))
            application.state = 'rejected'
            application.save()
        except CourseApplication.DoesNotExist:
            return Response({"error":"Course Application not found"},
                            status=status.HTTP_404_NOT_FOUND)

        return Response({"message":"Application to course rejected succesfully"}, 
                        status=status.HTTP_200_OK)

    @classmethod    
    def accept(cls, learner_id, course_id, request, date):
        #accept application for course
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
                            status=status.HTTP_200_OK)
        else:
            state = application.state 
            if state == 'accepted':
                return Response({"error":"Application to course has already been accepted"},
                        status=status.HTTP_400_BAD_REQUEST)
            
            application.state = 'accepted' 
            application.save()
        
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