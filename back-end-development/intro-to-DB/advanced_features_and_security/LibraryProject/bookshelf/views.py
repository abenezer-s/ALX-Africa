from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm

@permission_required('book_shelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'list_template.html', {'objects': books})

@permission_required('book_shelf.can_edit', raise_exception=True)
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

@permission_required('book_shelf.can_update', raise_exception=True)
def update_view(request, pk):
    obj = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('list_view')
    return redirect('edit_view', pk=pk)

@permission_required('book_shelf.can_delete', raise_exception=True)
def delete_view(request, pk):
    obj = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('list_view')
    return render(request, 'delete_template.html', {'object': obj})
