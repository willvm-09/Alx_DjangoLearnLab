from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer
from notifications.models import Notification


# Get the custom user model
User = get_user_model()

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Create the user using the validated data
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],  # Password will be automatically hashed
                bio=serializer.validated_data.get('bio', ''),  # Default to empty bio if not provided
                profile_picture=serializer.validated_data.get('profile_picture', None)
            )
            
            # Create a token for the user
            token = Token.objects.create(user=user)
            
            # Return the token as a response
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            # Authenticate the user (returns a user object if valid)
            user = authenticate(
                username=serializer.validated_data['username'], 
                password=serializer.validated_data['password']
            )
            
            if user is not None:
                # Get or create a token for the user
                token, created = Token.objects.get_or_create(user=user)
                
                # Return the token
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CustomUser

class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        CustomUser.objects.all()
        request.user.following.add(user_to_follow)

        Notification.objects.create(
            recipient=user_to_follow,
            actor=request.user,
            verb='started following you',
            target=None
        )
        return Response({'status': 'following', 'user': user_to_follow.username}, status=status.HTTP_200_OK)

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
        request.user.following.remove(user_to_unfollow)
        return Response({'status': 'unfollowed', 'user': user_to_unfollow.username}, status=status.HTTP_200_OK)


