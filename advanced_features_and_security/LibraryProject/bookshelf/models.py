from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#from .models import UserProfile, Author
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        permissions = [
            ('can_view', 'Can view'),
            ('can_create', 'Can create'),
            ('can_edit', 'Can edit'),
            ('can_delete', 'Can delete')
        ]

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    class Meta:
        permissions = [
            ('can_add_book', 'Can add a book'),
            ('can_change_book', 'Can change a book'),
            ('can_delete_book', 'Can delete a book'),
        ]

    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=200)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, profile_photo=None, date_of_birth=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, profile_photo=profile_photo, date_of_birth=date_of_birth, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, profile_photo=None, date_of_birth=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, profile_photo, date_of_birth, password)
    
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    profile_photo = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

# Get or create a group
editors_group, created = Group.objects.get_or_create(name='Editors')
viewers_group, created = Group.objects.get_or_create(name='Viewers')
admins_group, created = Group.objects.get_or_create(name='Admins')

#Fetch model with permissions
content_type = ContentType.objects.get_for_model(Author)

# Create permissions from Author Model
can_create = group.permissions.add(codename="can_create", name="Can create")
can_edit = group.permissions.add(codename="can_edit", name="Can edit")
can_view = group.permissions.add(codename="can_view", name="Can view")
can_delete = group.permissions.add(codename="can_delete", name="Can delete")

#Assign permissions
admins_group.permissions.add(can_view, can_create, can_edit, can_delete)
editors_group.permissions.add(can_create, can_edit)
viewers_group.permissions.add(can_view)

#Save groups and their permissions
admins_group.save()
editors_group.save()
viewers_group.save()