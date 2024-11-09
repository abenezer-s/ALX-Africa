from django.db.models import Q
from rest_framework.response import Response
from users.models import ProgramEnrollment, CourseEnrollment, UserProfile
from program.models import Program

def check_enrollments(user_profile, module):
    """
    Checks enrollment of learner in the course the module belongs to,
    as well as the prorams the course belongs to.
    """
    is_part_prog = None
    modules_course = module.course
    #check if course blongs to a program
    try:
        #course might be part of multiple programs
        course_programs = Program.objects.filter(courses=modules_course)
        is_part_prog = True
    except Program.DoesNotExist:
        is_part_prog = False
    #check users enrollment in course
    try:
        CourseEnrollment.objects.get(Q(course=modules_course) & Q(learner=user_profile))
        in_course = True
    except CourseEnrollment.DoesNotExist:
        in_course = False
    #check if user is enrolled to any program that conatains the course
    in_program = None
    if is_part_prog:
        # if user enrolled into atleast one program that conatins the module's course break and assign user as enrolled.
        for program in course_programs:
            try:
                prog_enrollment = ProgramEnrollment.objects.get(Q(program=program) & Q(learner=user_profile))
            except ProgramEnrollment.DoesNotExist:
                in_program = False
                continue
            
            else:
                in_program = True
                break

    return  in_course, in_program
 
def create_response(user_profile, in_course, in_program, user, module_owner, obj):
    """
    Creates apporiate messages.
    """
    if in_course or in_program or (module_owner == user):
        if in_course:
            return Response({"message": "Allowed",
                             "enrl": True})
        elif in_program:
            return Response({"message": "Allowed",
                             "enrl": True})
        else:
            return Response({"message": "Allowed",
                             "enrl": False})
    else:    
        if user_profile.creator:
            message = f"Access Denied. You do not own the course or program this {obj} belongs to."
            return Response({"error": message,
                             "message":False})
        
        message = f"You are not enrolled. Can not access this {obj}."  
        return Response({"error": message,
                         "message":False})

def enrolled_owner(module, user, obj):
        """
        A helper function to determine whether a user owns or,
        is enrolled in a program or a course the module belongs to.
        returns "Allowed" for 'message' field if so.
        returns "True" for 'enrl' field if enrolled in course or program.
        returns error messages otherwise.
        """
        module_owner = module.owner
        user_profile = UserProfile.objects.get(user=user)
        #check enrollments
        in_course, in_program = check_enrollments(user_profile, module)
        #grant access if enrolled to either the course or the program or user owns the moudle
        obj = obj
        #create appropriate messages
        message = create_response(user_profile, in_course, in_program, user, module_owner, obj)
        return message
        