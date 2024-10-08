from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio', 'profile_picture']
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only
        }

    def create(self, validated_data):
        # No need to override here since we're handling user creation in the view
        pass

from rest_framework import serializers

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'profile_picture', 'followers']
        read_only_fields = ['username', 'followers']

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        return instance
    
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

# Create a new user
user = get_user_model().objects.create_user(
    username='newuser', 
    email='newuser@example.com', 
    password='password123',
    bio='I love Django',
    profile_picture='path/to/profile_picture.jpg'
)

# Create a token for the newly created user
token = Token.objects.create(user=user)

# Output the token key
print(f"Token for {user.username}: {token.key}")
