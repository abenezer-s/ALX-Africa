from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.response import Response
from course.models import Course
from program.models import Program
from rest_framework import status

def complete_enrolling(counted):
    if counted:
        message = 'Application to program accepted succesfully. Leaner enrolled in program and course(s) within the program'  
        return Response({"message": message},
                        status=status.HTTP_200_OK)
    else:
        return Response({"message":"Application to program accepted succesfully"},
            status=status.HTTP_200_OK)
    
def assign_objects(obj, objApp):
    """
    assign objects appropriatly
    """
    Object = None
    ObjectApplication = None
    if obj == 'course':
        Object = Course
        ObjectApplication = objApp
    else:
        Object = Program
        ObjectApplication = objApp
    response = {"object":Object,
            "object_application":ObjectApplication}
    return response

def run_checks(user, learner_id, course_id, obj, objApp):
    """
    Check if application to course or program is not already accepted, 
    user has permission to accept
    """
    response = assign_objects(obj, objApp)
    Object = response['object'] # Course or Program

    ObjectApplication = response['object_application'] # CourseApplication or ProgramApplication
    try:
        learner = User.objects.get(id=learner_id)
        object_instance = Object.objects.get(id=course_id)
        
    except (User.DoesNotExist, Object.DoesNotExist):
        return Response({"error":"no object or learner found by the provided object or learner id"},
                        status=status.HTTP_404_NOT_FOUND)
    object_owner = object_instance.owner
    if object_owner != user:
        return Response({"error":"You do not have permission to perform this action"},
                        status=status.HTTP_401_UNAUTHORIZED)
    application = None
    try:
        if Object == Course:
            application = ObjectApplication.objects.get(Q(course=object_instance) & Q(learner=learner))
        else:
            application = ObjectApplication.objects.get(Q(program=object_instance) & Q(learner=learner)) 
    except ObjectApplication.DoesNotExist:
        msg = f"{Object} application not found"
        return Response({"error":msg},
                        status=status.HTTP_200_OK)
    else:
        state = application.state 
        if state == 'accepted':
            return Response({"error":"Application has already been accepted"},
                    status=status.HTTP_400_BAD_REQUEST)
        
    return Response({"error":False,
                     "application": application,
                     "object":object_instance,
                     "learner":learner})
