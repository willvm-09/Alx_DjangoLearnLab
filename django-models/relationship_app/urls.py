from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('relationship_app/', list_books, name='list_books'),
    path('relationship_app/', LibraryDetailView.as_view(), name='library_detail')
]