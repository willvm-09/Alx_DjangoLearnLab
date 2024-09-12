from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

# class UserManager(BaseUserManager):
#     def create_user(self, email, password):
#         if not email:
#             raise ValueError('Email is required')
#         user = user.model(email=self.normalize_email(email))
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password):
#         user = user.create_user(email=email, password=password)
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user

# class User(AbstractUser):
#     email = models.EmailField(unique=True, max_length=255)
#     username = models.CharField(unique=False, max_length=25)
#     objects = UserManager()
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['USERNAME_FIELD', 'password']

#     def __str__(self):
#         return self.username

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)

    def __str__(self):
        return self.title
