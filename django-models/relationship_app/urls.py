from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('relationship_app/', views.list_books, name='list_books'),
    path('relationship_app/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('login/', auth_views.LoginView.as_view(template_name=""), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name=""), name='logout'),
    path('register/', views.register, name='register'),
]
    
