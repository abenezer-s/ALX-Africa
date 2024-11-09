from django.db.models import Q
from decimal import Decimal
from django.db import models
from module.models import Module
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from utils import enrolled_owner

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
    
    @classmethod
    def validate(cls, learner_id, quiz_id, request):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except (Quiz.DoesNotExist):
            return Response({"error": "Quiz not found"},
                             status=status.HTTP_404_NOT_FOUND)
        try:
            learner = User.objects.get(id=learner_id)
        except User.DoesNotExist:
            return Response({"error": "learner not found"}, 
                            status=status.HTTP_404_NOT_FOUND)
        user = request.user
        module = quiz.module
        response = enrolled_owner(module, user, "quiz")
        #check if user is the actual learner and is enrolled or owns the module
        if response.data['message'] == 'Allowed'  and (learner == user):
            # Assume the request data contains the answers for each question
            answers = request.data.get('answers', [])
            questions_count = quiz.num_of_questions
        else:
            return  Response({
                "error":"can not perform this action."
            }, status=status.HTTP_403_FORBIDDEN)
    
        return Response({"error":False,
                        "learner":learner,
                        "answers":answers,
                        "module":module,
                        "quiz":quiz,
                        "questions_count":questions_count,})
    
    @classmethod
    def score_answers(cls, answers, learner, questions_count):
        """
        Check submmited answers validity.
        """
        correct_count = 0
        for answer_data in answers:
            try:
                question = Question.objects.get(id=answer_data['question_id'])
            except Question.DoesNotExist:
                continue  # Skip if the question does not exist
            submitted_ans = answer_data['submitted_ans']
            is_correct = (submitted_ans == question.answer)
            # Save the learner's answer
            LearnerAnswer.objects.create(learner=learner,
                                        question=question,
                                        answer=submitted_ans,
                                        correct=is_correct)
            if is_correct:
                correct_count += 1
        # Calculate the grade percentage
        grade = round(float(correct_count) / float(questions_count), 2) * 100 if questions_count > 0 else 0
        return grade
    
class Grade(models.Model):
    """
    model to store grades of learners.
    """
    module =  models.ForeignKey(Module, default=None, on_delete=models.CASCADE, related_name='module_grade')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_grade', blank=True, null=True)
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learner_grade')
    grade = models.DecimalField(blank=False, max_digits=5, decimal_places=2)
    passed = models.BooleanField(default=None)

    @classmethod
    def register_grade(cls, grade, module, learner, quiz):
        """
        Register learners grade, if previously attempted and
        score is better create a new grade and delete old grade.
        """ 
        try:
            instance = Grade.objects.get(Q(learner=learner) & Q(quiz=quiz))
        except Grade.DoesNotExist:
            pass
        else:
            prev_grade = instance.grade
            if grade <= prev_grade:
                return  Response({"error":"current grade not an improvement."},
                                 status=status.HTTP_200_OK)
            else:
                instance.delete() 
        passed = grade >= quiz.pass_score    
        if passed:
            #update grade records pass
            Grade.objects.create(module=module, 
                                quiz=quiz, 
                                learner=learner,
                                grade=grade, 
                                passed=True)
        else:
            #update grade records fail
            Grade.objects.create(module=module, 
                                 quiz=quiz, 
                                 learner=learner,
                                 grade=grade, 
                                 passed=False)
        return Response({
            "learner": learner.first_name,
            "grade": grade,
            "passed": passed
        }, status=status.HTTP_200_OK)

class LearnerAnswer(models.Model):
    """
    model to keep track of learner answers.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    learner = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()
    correct = models.BooleanField()
    
