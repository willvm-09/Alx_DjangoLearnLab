from .models import Author, Book, Library, Librarian

#Query all books by a specific author

author = Author.objects.get(author_name)
books_by_author = Book.objects.filter(author=author)

#List all books in a library

library = Library.objects.get(name=library_name)
books_in_library = library.books.all()

#Retrieve the librarian from a library

library = Library.objects.get(name=library_name)
librarian = Librarian.objects.get(library=library)