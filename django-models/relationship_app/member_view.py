
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render


def is_member(user):
    return user.userprofile.role == 'Member'
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')
