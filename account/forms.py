from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email','username','phone_number','gender','birth_day','password1', 'password2']
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'ایمیل',
            'phone_number': 'شماره تلفن',
            'birth_day': 'تاریخ تولد',
            'city': 'شهر',
            'address': 'آدرس',
            'gender':'جنسیت',
            'image': 'تصویر',
        }
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ( 'email','username','phone_number')

class MyLoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs = {"placeholder": "موبایل یا ایمیل"}))
    password = forms.CharField(widget=forms.PasswordInput())