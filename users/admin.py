from django.contrib import admin

from .models import User
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    
    search_fields = ('email','last_name','first_name',)
    list_filter = ('email','is_staff','is_active',)
    ordering = ('-date_joined',)
    list_display = ('email','first_name','last_name','date_of_birth','phone_number','is_active','is_staff',)
    fieldsets = (
        (None, {'fields':('email','first_name','last_name',)}),
        ('Permissions',{'fields':('is_staff','is_active')}),
        ('Personal',{'fields':('date_of_birth','phone_number',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':('email','first_name','last_name','date_of_birth','phone_number','password1','password2','is_staff','is_active',)
        }),
    )
    

admin.site.register(User, CustomUserAdmin)
