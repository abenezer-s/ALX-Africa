from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm

@permission_required
def list_view(request):
    objects = Book.objects.all()
    return render(request, 'list_template.html', {'objects': objects})

@permission_required
def edit_view(request, pk):
    obj = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('list_view')
    else:
        form = BookForm(instance=obj)
    return render(request, 'edit_template.html', {'form': form})

def update_view(request, pk):
    obj = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('list_view')
    return redirect('edit_view', pk=pk)

def delete_view(request, pk):
    obj = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('list_view')
    return render(request, 'delete_template.html', {'object': obj})
