from django.contrib import admin
from .models import UserProfile
from .models import Book, Author, Librarian, Library
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
admin.site.register(UserProfile)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', )
    
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', )

class CustomUserAdmin(UserAdmin):
    # Fields to be used in displaying the User model.
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff', )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    # Fields to be used in the admin detail view (when editing a user)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'profile_photo', 'date_of_birth')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to be used in the add user form in the admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'profile_photo', 'date_of_birth'),
        }),
    )

    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(CustomUser, CustomUserAdmin)