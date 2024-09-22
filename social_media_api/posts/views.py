from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters import rest_framework as filters
from notifications.models import Notification

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a post or comment to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
    
class PostFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')  # Search by title
    content = filters.CharFilter(lookup_expr='icontains')  # Search by content

    class Meta:
        model = Post
        fields = ['title', 'content']

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = PostFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
        return super().get_permissions()
    
from rest_framework import generics
from .models import Post

class UserFeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the current user
        user = self.request.user
        # Return posts from users the current user follows
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Like
from notifications.models import Notification

class LikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        # Check if the user has already liked the post
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({'status': 'already liked'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the Like entry
        like = Like.objects.get_or_create(user=request.user, post=post)

        # Create a notification (optional)
        notification = Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked your post',
            target=post
        )

        return Response({'status': 'liked', 'post': post.title}, status=status.HTTP_201_CREATED)

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = generics.get_object_or_404(Post, pk=pk)

        # Find the like entry
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()

            return Response({'status': 'unliked', 'post': post.title}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({'status': 'not liked'}, status=status.HTTP_400_BAD_REQUEST)


