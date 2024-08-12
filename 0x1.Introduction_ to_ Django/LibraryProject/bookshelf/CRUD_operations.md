#Create a Book instance

from bookshelf.models import Book
>>> new_book = Book(title="1984", author="George Orwell", publication_year=1949)
>>> new_book.save()
>>> retrieved_book = Book.objects.get(id=new_book.id)
>>> print(retrieved_book)
1984 by George Orwell published 1949


#Retrieve the book you created

retrieved_book = Book.objects.get(id=new_book.id)
>>> print(retrieved_book)
1984 by George Orwell published 1949

#Update title in Book 

from bookshelf.models import Book
>>> new_book.title = "Nineteen Eighty-Four"
>>> new_book.save()
>>> retrieved_book = Book.objects.get(id=new_book.id)
>>> print(retrieved_book)
Nineteen Eighty-Four by George Orwell published 1949

#Delete the book you created and confirm the deletion by trying to retrieve all books again.

new_book.delete()
(1, {'bookshelf.Book': 1})
>>> books = Book.objects.all()
>>> 
