from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='Confirm Password', 
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

from django import forms
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
