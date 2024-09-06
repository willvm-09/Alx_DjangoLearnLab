from django.db import models

# Create your models here.
#The Author model is serialized using the AuthorSerializer class in serializers.py
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

 #The Book model is serialized using the BookSerializer class in serializers.py   
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author')

    def __str__(self):
        return f'{self.title} by {self.author} published {self.publication_year}'
    


