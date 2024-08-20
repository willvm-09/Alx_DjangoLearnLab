from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=250)

class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

class Library(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book)

class Librarian(models.Model):
    name = models.CharField(max_length=200)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

