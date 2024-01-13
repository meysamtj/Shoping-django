from django.contrib import admin
from .models import CustomUser, Address, Otp_code
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email','phone_number']
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register((Address,Otp_code))