from django.urls import path
from . import views


urlpatterns = [
    path("/books/", views.ListView.as_view(), name="book_list"),
    path('/books/detail', views.DetailView.as_view(), name='book_details'),
    path('books/create/', views.CreateView.as_view(), name='create_books'),
    path('/books/update/', views.UpdateView.as_view(), name='update_book'),
    path('/books/delete/', views.DeleteView.as_view(), name='delete_books'),
]
