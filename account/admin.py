from django.contrib import admin
from .models import CustomUser, Address
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username','user_type', 'email', 'phone_number']
    fieldsets = UserAdmin.fieldsets + (
        ('Others', {'fields': ('user_type','birth_day', 'phone_number', 'image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type','email', 'birth_day', 'phone_number', 'image')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Address)
