from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import CustomUser
from django.utils.translation import gettext

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    
    list_display = ('name','family','mobile','email','gender','is_active','is_admin')
    list_filter = ('gender','is_active','is_admin')
    
    fieldsets = (
        (None,{'fields':('mobile','password','email')}),
        (gettext('Personal info'),{'fields':('name','family','gender')}),
        (gettext('Permissions'),{'fields':('is_active','is_admin','is_superuser','groups')}),
    )
    
    add_fieldsets = (
        (None,{'fields':('mobile','email','password1','password2')}),
    )
    
    search_fields = ('name','family','mobile')
    ordering = ('-is_active','-is_admin','family','name')
    filter_horizontal = ('groups',)