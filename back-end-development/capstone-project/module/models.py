from decimal import Decimal
from datetime import date
from django.db import models
from django.db.models import Q, Avg
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from course.models import Course
from program.models import Program
from users.models import CourseEnrollment, ProgramEnrollment

# Create your models here.
class Module(models.Model):
    owner = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='module_owner')
    name = models.CharField(max_length=150, blank=False, unique=True)
    content = models.TextField(default="default content", blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_module')
    created_at = models.DateField(blank=False)
    num_quizs = models.DecimalField(decimal_places=0, max_digits=2, default=0)

    def __str__(self) -> str:
        return self.name
    
    @classmethod
    def get_instances(cls, module_id, learner_id):
        try:
            learner = User.objects.get(id=learner_id)
        except User.DoesNotExist:
            return Response({"error":"learner not found"},
                            status=status.HTTP_404_NOT_FOUND)  
        try:
            module = Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            return Response({"error":"module does not exist"},
                            status=status.HTTP_404_NOT_FOUND)
        #proceed if module not already completed
        try:
            LearnerCompletion.objects.get(module=module, learner=learner)
        except LearnerCompletion.DoesNotExist:
            pass
        except LearnerCompletion.MultipleObjectsReturned:
            return Response({"error":"Module already completed"},
                            status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error":"Module already completed"},
                            status=status.HTTP_403_FORBIDDEN)
        return Response({"error" : False,
                        "learner": learner,
                        "module": module})
    
    @classmethod
    def calculate_score(cls, course, learner):
        from quiz.models import Grade
        #calculate course score 
        course_modules = Module.objects.filter(course=course)
        course_score = Decimal(0)
        num_modules = Decimal(0)
        for module_inst in course_modules:
            #module's score is the avg of all scores for quizs
            module_score = Grade.objects.filter(learner=learner, module=module_inst).aggregate(total=Avg('grade')) 
            course_score += module_score['total']
            num_modules += Decimal(1)
        return course_score / num_modules

    @classmethod
    def check_requirments(cls,module, learner, learner_profile):
        """
        Takes a module and its course, a learner and the profile.
        Returns and error if requirments have not be met or returns 
        a courseEnrollemnt object as a response.
        """
        from quiz.models import Grade
        module_course = module.course
        #check if enrolled in the course
        try:
            course_enrollment = CourseEnrollment.objects.get(Q(learner=learner_profile) & Q(course=module_course))          
        except CourseEnrollment.DoesNotExist:
            return Response({"error":"You do not have permisssion to perform this action. Not enrolled in course."},
                                    status=status.HTTP_403_FORBIDDEN)
        else:
            #check deadline
            date_today = date.today()
            deadline = course_enrollment.deadline
            if deadline:
                within_deadline = (deadline >= date_today)
                if not within_deadline:
                    return Response({"error":"Can not mark module as complete. Deadline has passed."},
                                    status=status.HTTP_403_FORBIDDEN)
        #check learner has passed all quizs in module then update progress
        num_quizs = module.num_quizs
        quizs_passed = 0
        if num_quizs > 0: 
            quizs_passed = Grade.objects.filter(learner=learner, module=module, passed=True).count()
            if num_quizs != quizs_passed:
                return Response({"error":"Can not mark module as complete. You have not passed all quizs."},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            #create a full score for module without quizes ensuring consistency
            Grade.objects.create(learner=learner,
                                 module=module,
                                 grade=100, 
                                 passed=True)
        return Response({"error":False,
                         "course_enrollment": course_enrollment})
    
    @classmethod
    def update_program_progress(cls, learner, module, course_enrollment, program_enrollments):
        """
        Update learner's progress possibly accross multiple programs.
        """
        date_today = date.today()
        #update each program that conatians the course and  learner is enrolled in
        message_list = []
        completed_progs = None
        for program_enrollment in program_enrollments: 
            #check dealine for program
            deadline = program_enrollment.deadline
            if deadline < date_today:
                #add message for program and continue
                prog_name = program_enrollment.program.name
                msg = {"message":"can not update progress. past deadline for program",
                        "program_name":program_name,
                        "score":course_score}
                message_list.append(msg)
                continue

            program_enrollment.number_of_courses_completed += Decimal(1)
            module_program = program_enrollment.program
            num_courses = module_program.number_of_courses
            completed_courses = program_enrollment.number_of_courses_completed
            if program_enrollment.progress != 100:
                progress = (completed_courses / num_courses) * 100
                program_enrollment.progress = progress
                cur_progress_program = program_enrollment.progress #current progress in program
                program_enrollment.save()
                if cur_progress_program == 100:
                    #learner has completed the program after finishing current course 
                    program_score = LearnerCompletion.complete_program(learner, module, program_enrollment)
                    course_score = LearnerCompletion.complete_course(learner, module, course_enrollment)
                    program_name = module_program.name
                    if course_score:
                        course_name = module.course.name
                        msg = {"message":"course completed",
                                "course_name":course_name,
                                "score":course_score}
                        message_list.append(msg)
                       
                    msg = {"message":"program completed",
                                "program_name":program_name,
                                "score":program_score}    
                    message_list.append(msg)
                    completed_progs = True

                else:
                    continue

        return message_list, completed_progs
    
    @classmethod
    def update_course_progress(cls, course_enrollment):
        """
        Update progres of the course the module belongs to.
        """
        course_enrollment.number_of_modules_completed += Decimal(1)
        module_course = course_enrollment.course
        num_modules = module_course.number_of_modules
        completed_modules = course_enrollment.number_of_modules_completed
        cur_course_progress = course_enrollment.progress #current progress in course
        if cur_course_progress != 100:
        #update course progress
            progress = (completed_modules / num_modules) * 100
            course_enrollment.progress = progress
            cur_course_progress = course_enrollment.progress 
            course_enrollment.save()
        return cur_course_progress
    
    @classmethod
    def make_progress(cls, learner, module, course_enrollment, program_enrollments=None):
        """
        Orcestrates learner's progress.
        """
        cur_course_progress = cls.update_course_progress(course_enrollment)
        #check if course is part of any program and update program progress if course is co7mpleted
        if (cur_course_progress == 100) and program_enrollments:
            message_list, completed_progs = cls.update_program_progress(learner, module, course_enrollment, program_enrollments)
            if completed_progs:
                # learner has completed atleast one program
                return Response({"message":message_list},
                                status=status.HTTP_200_OK)
            #learner has completed the course
            course_score = LearnerCompletion.complete_course(learner, module, course_enrollment)
            #return messages if any
            if message_list:
                return Response({"message":"course completed successfully! ",
                            "score":course_score,
                            "past_deadline_progs": message_list},
                            status=status.HTTP_200_OK)
            
            return Response({"message":"course completed successfully! ",
                            "score":course_score},
                            status=status.HTTP_200_OK)
            
        elif cur_course_progress != 100:
            #learner has only completed the module
            response = LearnerCompletion.complete_module(learner,module)
            return response
    
        else:
            #learner has completed the course
            course_score = LearnerCompletion.complete_course(learner, module, course_enrollment)
            return Response({"message":"course completed successfully. ",
                             "score": course_score},
                             status=status.HTTP_200_OK)

    @classmethod
    def update_progress(cls, learner, learner_profile, module, course_enrollment):
        """
        Update learner's progress in course and accross enrolled programs 
        that the course might be part of.
        """
        #get all programs the course could be part of
        module_course = module.course
        module_programs = Program.objects.filter(courses__name=module_course.name)    
        if not module_programs:
            #course not part of any program
            update = cls.make_progress(learner, module, course_enrollment)
            return update
        #course is part of atleast one program
        program_enrollment_list = []
        for program in module_programs:
            try:
                program_enrollment = ProgramEnrollment.objects.get(learner=learner_profile, program=program)
            except ProgramEnrollment.DoesNotExist:
                #learner not enrolled in program
                continue
            program_enrollment_list.append(program_enrollment)
        #if course is part of atleast one program and learner is enrolled in it,  update program progress
        if program_enrollment_list:  
            update = cls.make_progress(learner, module, course_enrollment, program_enrollment_list)
            return update
        else:
            #learner is not enrolled in any program the course is part of
            update = cls.make_progress(learner, module, course_enrollment)
            return update    

class Media(models.Model):
    owner = models.ForeignKey(User,default=None, on_delete=models.CASCADE, related_name='media_owner')
    name = models.CharField(max_length=20, unique=True, default="file name", blank=False)
    file = models.FileField(upload_to='media/')
    description = models.CharField(max_length=255, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='module_media')

class LearnerCompletion(models.Model):
    """
    Model to keep track of a learner's completion of programs and courses.
    Therefore making them eligible for a certificate if learner has an instance of this model
    """
    learner = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, null=True,default=None, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True,default=None, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, null=True,default=None, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    completed_at = models.DateField()

    @classmethod
    def complete_program(cls, learner, module, program_enrollment):
        """
        Complete a program for learner.
        """
        date_today = date.today()
        module_course = module.course
        module_program = program_enrollment.program
        #calculate program score
        program_courses = module_program.courses.all()
        prog_score = Decimal(0)
        count_course = Decimal(0)
        for course_inst in program_courses:
           #calculate course score
            course_score = Module.calculate_score(course_inst, learner) 
            prog_score += course_score
            count_course += Decimal(1)
        
        prog_score = prog_score / count_course 
        formated_score = format(prog_score, '.2f')    
        LearnerCompletion.objects.get_or_create(learner=learner, 
                                         module=module, 
                                         course=module_course,
                                         program=module_program, 
                                         score=formated_score, 
                                         completed_at=date_today)
        
        program_enrollment.status = 'completed'
        program_enrollment.save()

        return formated_score
    
    @classmethod
    def complete_course(cls, learner, module, course_enrollment):
        """
        Complete a course for learner.
        """
        date_today = date.today()
        module_course = module.course
        course_score = Module.calculate_score(module_course, learner) 
        formated_score = format(course_score, '.2f')
        if course_enrollment.status != 'completed':
            LearnerCompletion.objects.get_or_create(learner=learner, 
                                             module=module, 
                                             course=module_course, 
                                             completed_at=date_today, 
                                             score=course_score)

            course_enrollment.status = 'completed'
            course_enrollment.save()
            return formated_score
        
        return False
    
    @classmethod
    def complete_module(cls, learner, module):
        """
        Complete a module for learner.
        """
        from quiz.models import Grade
        date_today = date.today()
        result = Grade.objects.filter(learner=learner, module=module).aggregate(total=Avg('grade'))
        score = result['total']
        LearnerCompletion.objects.get_or_create(learner=learner,
                                          module=module, 
                                          score=score, 
                                          completed_at=date_today)
        return Response({"message":"module completed successfully! ",
                         "score":score},
                         status=status.HTTP_200_OK)