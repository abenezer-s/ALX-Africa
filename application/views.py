from datetime import datetime, timedelta
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from permissions import IsContentCreator, IsLearner
from .models import *
from .serializers import *
from application.serializers import (ProgramApplicationSerialzer,
                                    CourseApplicationSerialzer, 
                                    ResponseCourseSerializer, 
                                    ResponseProgramSerializer)

# Create your views here.
class ResponseCourse(APIView):
    """
    Given course id, learner's id and a response(accept/reject), 
    rejects or accepts application if it exists.
    """   
    permission_classes = [IsContentCreator]

    def post(self, request, learner_id, course_id):
        date = datetime.now()
        serializer = ResponseCourseSerializer(data=request.data)
        if serializer.is_valid():
            response = serializer.validated_data['response']
            if response.lower() not in ['accept', 'reject'] :
                return Response({"message":"response not recognized. Must be Accept or Reject."})
            
            #enroll learner to course/program if accepted            
            if response.lower() == 'accept':
                message = CourseApplication.accept(learner_id, course_id, request, date)
                return message
            else:
                message = CourseApplication.reject(learner_id, course_id, request)
                return message
        else:       
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class ResponseProgram(APIView):
    """
    Given program id, learner's id and a response(accept/reject), 
    rejects or accepts application if it exists.
    """   
    permission_classes = [IsContentCreator]
    
    def post(self, request, program_id, learner_id):
        date = datetime.now()
        serializer = ResponseProgramSerializer(data=request.data)
        if serializer.is_valid():
            
            response = serializer.validated_data['response']
            if response.lower() not in ['accept', 'reject']:
                return Response({"message":"response not recognized. Must be Accept or Reject."},
                                status=status.HTTP_400_BAD_REQUEST)
            
            #enroll learner to program if accepted            
            if response.lower() == 'accept':
                message = ProgramApplication.accept(learner_id,program_id, request, date)
                return message
            else:
                message = ProgramApplication.reject(learner_id, program_id, request)
                return message
        else:       
            pass


class ApplyCourse(APIView):
    """
    given course and learner id
    an Application instance will be created conatining the info.
    """
    permission_classes = [IsLearner]
    def post(self, request, course_id, learner_id):
        date = datetime.now()
        serializer = ApplyCourseSerializer(data=request.data)
        user = request.user
        response = CourseApplication.apply(user, course_id, learner_id, serializer, date)

        return response
    
class ApplyProgram(APIView):
    """
    given program and learner id
    an Application instance will be created conatining the info.
    """
    permission_classes = [IsLearner]
    def post(self, request, program_id, learner_id):
        date = datetime.now()
        serializer = ApplyProgramSerializer(data=request.data)
        user = request.user
        response = ProgramApplication.apply(user, program_id, learner_id, serializer, date)
        
        return response
    
class ProgramApplicationDetailAPIView(generics.RetrieveAPIView):
    queryset = ProgramApplication.objects.all()
    serializer_class = ProgramApplicationSerialzer
    permission_classes = [IsAuthenticated]


class ProgramApplicationListAPIView(generics.ListAPIView):
    queryset = ProgramApplication.objects.all()
    serializer_class = ProgramApplicationSerialzer
    permission_classes = [IsAuthenticated]
    #query set conatining only applications related to user (owner or learner)
    def get_queryset(self):
        query_set = ProgramApplication.objects.filter(Q(owner=self.request.user) | Q(learner=self.request.user))
        return query_set

class ProgramApplicationUpdateAPIView(generics.UpdateAPIView):
    queryset = ProgramApplication.objects.all()
    serializer_class = ProgramApplicationSerialzer
    permission_classes = [IsContentCreator]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.owner != request.user:
            raise PermissionDenied("You do not have permission to edit this application.")
        return super().update(request, *args, **kwargs)

class ProgramApplicationDestroyAPIView(generics.DestroyAPIView):
    queryset = ProgramApplication.objects.all()
    serializer_class = ProgramApplicationSerialzer
    permission_classes = [IsContentCreator]

    def destroy(self,request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this application.")
        instance.delete()
        return Response({"message": "application deleted successfully."},
                        status=status.HTTP_200_OK)

class CourseApplicationDetailAPIView(generics.RetrieveAPIView):
    queryset = CourseApplication.objects.all()
    serializer_class = CourseApplicationSerialzer
    permission_classes = [IsAuthenticated]


class CourseApplicationListAPIView(generics.ListAPIView):
    queryset = CourseApplication.objects.all()
    serializer_class = CourseApplicationSerialzer
    permission_classes = [IsAuthenticated]
    #query set conatining only applications related to user (owner or learner)
    def get_queryset(self):
        query_set = CourseApplication.objects.filter(Q(owner=self.request.user) | Q(learner=self.request.user))
        return query_set

class CourseApplicationUpdateAPIView(generics.UpdateAPIView):
    queryset = CourseApplication.objects.all()
    serializer_class = CourseApplicationSerialzer
    permission_classes = [IsContentCreator]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.owner != request.user:
            raise PermissionDenied("You do not have permission to edit this application.")
        return super().update(request, *args, **kwargs)

class CourseApplicationDestroyAPIView(generics.DestroyAPIView):
    queryset = CourseApplication.objects.all()
    serializer_class = CourseApplicationSerialzer
    permission_classes = [IsContentCreator]

    def destroy(self,request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this application.")
        instance.delete()
        return Response({"message": "application deleted successfully."},
                        status=status.HTTP_200_OK)
       