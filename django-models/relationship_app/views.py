from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from .models import Book
from .models import Library

# Create your views here.
def is_admin(user):
    return user.userprofile.role == 'Admin'
@user_passes_test(is_admin)
def admin_view(request):
    return HttpResponse('admin')

def is_librarian(user):
    return user.userprofile.role == 'Librarian'
@user_passes_test(is_librarian)
def librarian_view(request):
        return HttpResponse('librarian')


def is_member(user):
    return user.userprofile.role == 'Member'
@user_passes_test(is_member)
def member_view(request):
    return HttpResponse('member')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Log the user in
            login(request, user)
            return redirect('book-view')  # Redirect to a success page
        
    
    return render(request, "relationship_app/login.html")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def  list_books(request):
    qs = Book.objects.all()
    context = {
        'books' : qs
    }

    return render(request, 'relationship_app/list_books.html',context)

class LibraryDetailView(DetailView):
    model =Library
    template_name = 'relationship_app/library_detail.html'


#class SignUpView(CreateView):
#    form_class = UserCreationForm
#    success_url = reverse_lazy('login')
#    template_name = 'relationship_app/registration.html'
#
#
#
#class LibraryLogoutView(LogoutView):
#    next_page = 'relationship_app/login'  

