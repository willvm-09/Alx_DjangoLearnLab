
from django.urls import path
from .views import UserLoginView, UserLogoutView, RegisterView, profile_view

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile_view, name='profile'),
]

from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]

from . import views

urlpatterns = [
    path('post/<int:pk>/comments/new/', views.CommentCreateView, name='add_comment'),
    path('comment/<int:pk>/update/', views.CommentUpdateView, name='edit_comment'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView, name='delete_comment'),
]
