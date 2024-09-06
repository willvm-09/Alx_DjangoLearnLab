from .models import Author, Book
from rest_framework import serializers
import datetime

#This serializer serializes the Book model in models.py
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'title']

        def validate(self, data):
            if data['publication_year'] > datetime.date.today():
                raise serializers.ValidationError("Invalid Publication Year")
            return data
        
#This serializer serializes the Author model in models.py
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name']    