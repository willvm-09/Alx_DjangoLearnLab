from bookshelf.models import Book

new_book = Book(title="1984", author="George Orwell", publication_year="1949")
new_book.save()

new_book.delete()
books = Book.objects.all()