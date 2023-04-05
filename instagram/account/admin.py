# Django imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Instagram models
from instagram.account.models import User
from instagram.account.models import Profile


class CustomUserAdmin(UserAdmin):
    
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_verified'
    ]
    
    list_display_links = ['username', 'email']


admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    
    list_display = ['user']
    
    list_display_links = ['user']