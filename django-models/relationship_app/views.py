from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# Create your views here.

def list_books(request):
    books = Book.objects.all()
    context = {'list_books': books}
    return render(request, 'books/list_books.html', context)

class LibraryView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.books.all()
        return context



