from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
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
from django.forms import BookForm


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():

            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'bookshelf/register.html', {'form': form})


def book_list(request):
    books = Book.objects.all()
    context = {'list_books': books}
    return render(request, 'bookshelf/list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'bookshelf/library_detail.html'
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
    return render(request, 'bookshelf/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'bookshelf/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request,'bookshelf/member_view.html')



@permission_required('bookshelf.can_add_book')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/books/')
        else:
            form = BookForm()
        return render(request, 'bookshelf/add_book.html', {'form':form})
@permission_required('bookshelf.can_change_book')
def edit_book(request, id_book):
    book = Book.objects.get(pk=id_book)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid:
            form.save()
            return redirect('/books/')
        else:
            form = BookForm(instance=book)
        return render(request, 'bookshelf/edit_book.html', {'form': form, 'book': book})
@permission_required('bookshelf.can_delete_book')
def delete_book(request, id_book):
    book = Book.objects.get(pk=id_book)
    if request.method == 'POST':
        book.delete()
        return redirect('/books/')
    return render(request, 'bookshelf/edit_book.html', {'book': book})

@permission_required('bookshelf.can_create', raise_exception=True)
def create_author(request):
    if request.method == 'POST':
        # Form processing logic here
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm()
    return render(request, 'bookshelf/author_form.html', {'form': form})

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    if request.method == 'POST':
        # Form processing logic here
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author_detail', author_id=author.id)
    else:
        form = AuthorForm(instance=author)
    return render(request, 'bookshelf/author_form.html', {'form': form})

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    if request.method == 'POST':
        author.delete()
        return redirect('author_list')
    return render(request, 'bookshelf/author_confirm_delete.html', {'author': author})

@permission_required('bookshelf.can_view', raise_exception=True)
def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'booksheld/author_detail.html', {'author': author})

#In views.py, I added two extra functions to showcase how I would parameterize queries instead of string formatting.
#Validate and sanitize all user inputs using Django forms or other validation method
#This is by using the %s a placeholder for the actual value. Django safely inserts the user_input value into the query, ensuring that it is properly escaped and not interpreted as SQL code.

from .forms import ExampleForm

def example_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success_url')  # Redirect to a success page
    else:
        form = ExampleForm()
    
    return render(request, 'example_template.html', {'form': form})