from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView,CreateView
from django.views.generic.detail import DetailView
from .models import Library
from .models import Book

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse_lazy
from django.views import View
from .models import UserProfile
from typing import Any
from .forms import BookForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Replace 'home' with your desired redirect URL after registration
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


def list_books(request):
    books = Book.objects.all()
    context = {'list_books': books}
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.books.all()
        return context

#define custom test functions that check if the user has a specific role

def is_admin(user):
    return user.is_authenticated and user.userprofile.role == 'ADMIN'

def is_librarian(user):
    return user.userprofile.role == 'LIBRARIAN'

def is_member(user):
    return user.userprofile.role == 'MEMBER'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request,'relationship_app/member_view.html')



@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/books/')
        else:
            form = BookForm()
        return render(request, 'relationship_app/add_book.html', {'form':form})
@permission_required('relationship_app.can_change_book')
def edit_book(request, id_book):
    book = Book.objects.get(pk=id_book)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid:
            form.save()
            return redirect('/books/')
        else:
            form = BookForm(instance=book)
        return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})
@permission_required('relationship_app.can_delete_book')
def delete_book(request, id_book):
    book = Book.objects.get(pk=id_book)
    if request.method == 'POST':
        book.delete()
        return redirect('/books/')
    return render(request, 'relationship_app/edit_book.html', {'book': book})