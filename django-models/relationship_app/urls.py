from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import admin_view, librarian_view, member_view


urlpatterns = [
    path('relationship_app/', views.list_books, name='list_books'),
    path('relationship_app/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('login/', auth_views.LoginView.as_view(template_name=""), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name=""), name='logout'),
    path('register/', views.register, name='register'),
    path('relationship_app/', admin_view, name='admin_dashboard'),
    path('relationship_app/', librarian_view, name='librarian_dashboard'),
    path('relationship_app/', member_view, name='member_dashboard'),
]
    
