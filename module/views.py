from datetime import datetime, date
from django.db.models import Q, Sum, Avg
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from permissions import IsContentCreator, IsLearner
from .models import *
from users.models import CourseEnrollment, ProgramEnrollment, UserProfile
from .serializers import *
from decimal import Decimal
from utils import enrolled_owner

# Create your views here.
class MarkComplete(APIView):
    """
    Mark the module as completed and update overal progress on the program or course.
    """
    permission_classes = [IsAuthenticated]
   
    def post(self, request, module_id, learner_id):
        
        user = self.request.user
        # get learner and module instances
        response = Module.get_instances(module_id, learner_id)
        if response.data['error']:
            #errors while getting instances
            return response
    
        learner = response.data['learner']
        module = response.data['module']
        learner_profile = UserProfile.objects.get(user=learner)
        course_enrollment = None 

        #check if user has completed all requirments
        response = Module.check_requirments(module, learner, learner_profile)
        if response.data['error']:
            # has not passed requirment checks
            return response
        else:
           course_enrollment = response.data['course_enrollment']

        #if learner has passed requirment checks or user is owner of module, update progress
        if (learner_profile.creator == False) or (user == module.owner):
            response = Module.update_progress(learner, learner_profile, module, course_enrollment)
            return response     
        else:
            return Response({"error":"you do not have permisssion to perform this action"},
                                status=status.HTTP_403_FORBIDDEN)

class ModuleDetailAPIView(generics.RetrieveAPIView):

    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer
    permission_classes = [IsAuthenticated]
    
    #check if the user is enrolled or owns the module if so grant access
    def get(self, request, *args, **kwargs):
        
        module = self.get_object()
        user = request.user
        response = enrolled_owner(module, user, 'module')
        
        #grant access if enrolled to either the course or the program or user owns the moudle
        if response.data['message'] == 'Allowed':
            return super().get(request, *args, **kwargs)
        else:
            return response

class ModuleCreateAPIView(generics.CreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer
    permission_classes = [IsAuthenticated, IsContentCreator] 

    # create  module assign it to a course and update course info
    def create(self, request, course_id, *args, **kwargs):
        date = datetime.now()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
        
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return Response({"error": "course does not exist"},
                                status=status.HTTP_404_NOT_FOUND)
            
            if course.owner == self.request.user: 
                Module.objects.create(owner=self.request.user,
                                    course=course,
                                    name=name, 
                                    created_at=date)
                  
                num_modules = course.number_of_modules          #update number of modules field to reflect chnage
                num_modules += Decimal(1)
                course.number_of_modules = num_modules
                course.save()
                return Response({"message": "module created succesfully"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "you do not have permission to perform this action"},
                                status=status.HTTP_403_FORBIDDEN)
            
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

class ModuleListAPIView(generics.ListAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        query_set = Module.objects.filter(owner=user)
        return query_set
  
class ModuleUpdateAPIView(generics.UpdateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer
    permission_classes = [IsContentCreator]

    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.owner != request.user:
            raise PermissionDenied("You do not have permission to edit this module.")
        return super().update(request, *args, **kwargs)
    
class ModuleDestroyAPIView(generics.DestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer
    permission_classes = [IsContentCreator]

    def destroy(self, request, *args, **kwargs ):
        instance = o=self.get_object()
        # Check ownership
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this quiz.")
        
        course = instance.course
        num_mod = course.number_of_modules
        num_mod -= Decimal(1)
        course.number_of_modules = num_mod
        course.save()
        instance.delete()
        return Response({"message": "Module deleted successfully."},
                        status=status.HTTP_200_OK)

class MediaDetailAPIView(generics.RetrieveAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerialzer 
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        
        media = self.get_object()
        module = media.module
        user = request.user 
        response = enrolled_owner(module, user, 'media')
        
        #grant access if enrolled to either the course or the program or user owns the moudle
        if response.data['message'] == 'Allowed':
            return super().get(request, *args, **kwargs)
        else:
            return response

class MediaCreateAPIView(generics.CreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerialzer
    permission_classes = [IsContentCreator] 

    def create(self, request, module_id):

        serializer = MediaSerialzer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data["file"]
            description = serializer.validated_data["description"]
            name = serializer.validated_data["name"]
            user = request.user
            try:
                module = Module.objects.get(id=module_id)
            except Module.DoesNotExist:
                return Response({"message":"Can not add media to module. Module does not exist."},
                                 status=status.HTTP_404_NOT_FOUND)
            
            #create media instance if user owns the module
            if user == module.owner:
                Media.objects.create(owner=user, name=name, file=file, description=description, module=module)
                return Response({"message":"Added media to module successfully."},
                                status=status.HTTP_200_OK)
            else: 
                return Response({"error":"Can not add media to module. You do not have permission."},
                                status=status.HTTP_403_FORBIDDEN)
        
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

class MediaListAPIView(generics.ListAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerialzer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        query_set = Media.objects.filter(owner=user)
        return query_set
        
class MediaUpdateAPIView(generics.UpdateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerialzer
    permission_classes = [IsContentCreator]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.owner != request.user:
            raise PermissionDenied("You do not have permission to edit this media.")
        return super().update(request, *args, **kwargs)


class MediaDestroyAPIView(generics.DestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerialzer
    permission_classes = [IsContentCreator]

    def destroy(self,request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this quiz.")
        instance.delete()
        return Response({"message": "Media deleted successfully."},
                        status=status.HTTP_200_OK)
    
