from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'bio', 'profile_picture')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'profile_picture', 'followers')}),
    )   
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'profile_picture')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
