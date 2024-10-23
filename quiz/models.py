from decimal import Decimal
from django.db import models
from module.models import Module
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status

# Create your models here.
class Quiz(models.Model):
    """
    a model to store quizs for a module with optional time limits.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=30, default='default test name', unique=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='module_quiz',default=None)
    description = models.TextField(blank=False)
    pass_score = models.DecimalField(default=50, blank=True, max_digits=3, decimal_places=0)
    num_of_questions = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    created_at = models.DateField(blank=True, default=None)

    @classmethod
    def create_quiz(cls, module_id, serializer, date, user):
        if serializer.is_valid():
            description = serializer.validated_data['description']
            pass_score = serializer.validated_data['pass_score']
            name = serializer.validated_data['name']

            try:
                module = Module.objects.get(id=module_id)
            except Module.DoesNotExist:
                return Response({"error": "module does not exist"},
                                status=status.HTTP_404_NOT_FOUND)
            
            if module.owner == user: 
                try:
                    Quiz.objects.create(owner=user, 
                                    module=module, 
                                    name=name,
                                    description=description,
                                    pass_score=pass_score, 
                                    created_at=date)  
                except IntegrityError:
                    return Response({"error":"quiz with that name exists"})
                
                num_quizs = module.num_quizs
                num_quizs += Decimal(1)
                module.num_quizs = num_quizs
                module.save()
                return Response({"message": "quiz created succesfully"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error": "you do not have permission to perform this action"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        
    
class  Question(models.Model):
    """
    A model used to model a question which is part of the quiz model. 
    Must have muliple potetnial answers if question is multiple choice( multi=True)
    """
    quiz = models.ForeignKey(Quiz, default=None, on_delete=models.CASCADE, related_name='quiz_question')
    value = models.TextField(default=None, blank=False)
    multi = models.BooleanField(blank=False)     #feild to determine wheter the question is multiple choice or fill in blank
    answer = models.TextField(blank=False)
    created_at = models.DateField(blank=True, default=None)

class Answer(models.Model):
    """
    potential answer to a question
    """
    choice_number = models.DecimalField(default=None, blank=False, max_digits=1, decimal_places=0) # the choice number in the possible avaible choices
    value = models.TextField(blank=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices', default=None)
    created_at = models.DateField(default=None)

class Grade(models.Model):
    """
    model to store grades of learners.
    """
    module =  models.ForeignKey(Module, default=None, on_delete=models.CASCADE, related_name='module_grade')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_grade', blank=True, null=True)
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learner_grade')
    grade = models.DecimalField(blank=False, max_digits=5, decimal_places=2)
    passed = models.BooleanField(default=None)

class LearnerAnswer(models.Model):
    """
    model to keep track of learner answers.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    learner = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()
    correct = models.BooleanField()
    
