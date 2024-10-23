from rest_framework import serializers
from .models import *

class ApplyCourseSerializer(serializers.Serializer):
    
    motivation_letter = serializers.CharField()

class ApplyProgramSerializer(serializers.Serializer):
    
    motivation_letter = serializers.CharField()

class ApplicationResponseCourseSerializer(serializers.Serializer):
    
    response = serializers.CharField()
    class Meta:
        model = CourseApplication
        fields = [
            'owner' ,
            'learner' ,
            'motivation_letter' ,
            'submitted_at' ,
            'course' ,
            'state',
            'response'
        ]

        read_only_field = ['owner', 'learner','submitted_at', 'course', 'state']

class ApplicationResponseProgramSerializer(serializers.Serializer):
    response = serializers.CharField()
    class Meta:
        model = ProgramApplication
        fields = [
            'owner' ,
            'learner' ,
            'motivation_letter',
            'submitted_at' ,
            'program' ,
            'state' 
            
        ]

        read_only_field = ['owner', 'learner','submitted_at', 'program', 'state']

class ProgramApplicationSerialzer(serializers.ModelSerializer):
    class Meta:
        model = ProgramApplication
        fields = '__all__'

class CourseApplicationSerialzer(serializers.ModelSerializer):
    class Meta:
        model = CourseApplication
        fields = '__all__'