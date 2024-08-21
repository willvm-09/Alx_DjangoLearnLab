from django.shortcuts import render

# Create your views here.

from relationship_app.models import Book

def book_list(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

from django.views.generic.detail import DetailView
from .models import Library

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(library=self.object)
        return context

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile

def is_admin(user):
    return user.is_authenticated and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.userprofile.role == 'Librarian'

def is_member(user):
    return user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request,'member_view.html')

from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm

@permission_required('relationship_app.add_book')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect('library_detail', pk=book.library.pk)
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

@permission_required('relationship_app.delete_book')
def edit_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('library_detail', pk=book.library.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form})

class register(CreateView):
    form_class = UserCreationForm()
    success_url = reverse_lazy('login')
    template_name = 'relationship_app/register.html'
    
def login (request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/books/')  #redirects user towards the books page.
            else:
                return HttpResponse("Invalid credentials", status=401)
        else:
            return HttpResponse("Invalid form data", status=400)
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})
    
def index(request):
    return render(request, 'relationship_app/index.html')


def check_role(user, role):
  return user.is_authenticated and user.userprofile.role == role

@user_passes_test(lambda user: check_role(user, "Admin"))
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

@user_passes_test(lambda user: check_role(user, "Librarian"))
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

@user_passes_test(lambda user: check_role(user, "Member"))
def member_view(request):
    return render(request, "relationship_app/member_view.html")

@permission_required('relationship_app.delete_book')
def delete_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('library_detail', pk=book.library.pk)
    return render(request, 'relationship_app/delete_book.html', {'book': book})


from typing import Any
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Library,Book
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.views.generic import DetailView,TemplateView,ListView, CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import permission_required
from .forms import BookForm
# Create your views here.
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
def list_books (request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request,'relationship_app/list_books.html',context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
# Create your views here.
class register(CreateView):
    form_class = UserCreationForm()
    success_url = reverse_lazy('login')
    template_name = 'relationship_app/register.html'
    
def login (request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/books/')  #redirects user towards the books page.
            else:
                return HttpResponse("Invalid credentials", status=401)
        else:
            return HttpResponse("Invalid form data", status=400)
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})
    
def index(request):
    return render(request, 'relationship_app/index.html')

def check_role(user, role):
  return user.is_authenticated and user.userprofile.role == role

@user_passes_test(lambda user: check_role(user, "Admin"))
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

@user_passes_test(lambda user: check_role(user, "Librarian"))
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

@user_passes_test(lambda user: check_role(user, "Member"))
def member_view(request):
    return render(request, "relationship_app/member_view.html")