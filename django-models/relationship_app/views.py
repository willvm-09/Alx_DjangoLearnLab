from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Library
from .models import Book

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator

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

class Admin:
    def __call__(self, user):
        return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

class Librarian:
    def __call__(self, user):
        return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

class Member:
    def __call__(self, user):
        return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


#create separate views for each role and apply the @user_passes_test decorator to ensure only users with the appropriate role can access each view.

@method_decorator(user_passes_test(is_admin, login_url='/login/'), name='dispatch')
class AdminView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Welcome, Admin! This is your dashboard.")

@method_decorator(user_passes_test(is_librarian, login_url='/login/'), name='dispatch')
class LibrarianView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Welcome, Librarian! Here you can manage the library.")

@method_decorator(user_passes_test(is_member, login_url='/login/'), name='dispatch')
class MemberView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Welcome, Member! Enjoy your membership benefits.")