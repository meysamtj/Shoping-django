from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    # password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'phone_number', 'gender', 'birth_day', 'password1',
                  'password2']
        # labels = {
        #     'first_name': 'نام',
        #     'last_name': 'نام خانوادگی',
        #     'email': 'ایمیل',
        #     'phone_number': 'شماره تلفن',
        #     'birth_day': 'تاریخ تولد',
        #     'city': 'شهر',
        #     'gender': 'جنسیت',
        #     'image': 'تصویر',
        # }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'phone_number')


class UserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'phone_number', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'phone_number', 'image', 'gender', 'birth_day', 'national_code')


class PasswordForm(forms.Form):
    password_before = forms.CharField(label="Your password", required=True
                                      , widget=forms.PasswordInput())
    password_new = forms.CharField(label="New password", required=True
                                   , widget=forms.PasswordInput())
    password_again = forms.CharField(label="Confirm password", required=True
                                     , widget=forms.PasswordInput())

    # def clean_password_before(self):
    #     password = self.cleaned_data.get('password_before')
    #     if self.request.user.check_password(password):
    #         raise ValidationError(" password is wrong")
    #     return password

    def clean(self):
        result = super().clean()
        password1 = result.get('password_new')
        password2 = result.get('password_again')
        if password1 and password1 and password1 != password2:
            raise ValidationError("password must be match")
        return result
