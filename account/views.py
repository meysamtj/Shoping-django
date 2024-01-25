from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, RedirectView, ListView, DetailView, FormView, CreateView, DeleteView, \
    UpdateView
from django.contrib.auth import login, authenticate, logout
from .forms import UserCreateForm, ProfileForm, PasswordForm
from .models import CustomUser
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .otpcode import OTPGenerator


class Login(View):
    template_class = "account/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:home")
        else:
            return super().dispatch(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs) -> None:
        self.next = request.GET.get("next")
        request.session["next"] = self.next
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        print(request.session.get('username'))
        return render(request, self.template_class)

    # def post(self, request):
    #     if request.POST.get("email"):
    #         if request.POST.get("pass"):
    #             email = request.POST.get("email")
    #             password = request.POST.get("pass")
    #             user = authenticate(username=email, password=password)
    #             if user:
    #                 login(request, user)
    #                 if self.next:
    #                     return redirect(self.next)
    #                 return redirect("core:home")
    #             else:
    #                 messages.success(request, 'User Or Password is Wrong ', 'danger')
    #                 return render(request, self.template_class)
    #         else:
    #             messages.success(request, 'field password Is Empty ', 'danger')
    #             return render(request, self.template_class)
    #     else:
    #         messages.success(request, 'field email or phone Is Empty ', 'danger')
    #         return render(request, self.template_class)
    def post(self, request):
        if request.POST.get("email"):
            email = request.POST.get("email")
            user = CustomUser.objects.filter(Q(username=email) | Q(phone_number=email)).exists()
            email = CustomUser.objects.filter(email=email).exists()
            # if request.session.get("username"):
            #     del request.session['username']
            # if request.session.get("email"):
            #     del request.session['email']
            if user:
                request.session["username"] = request.POST.get("email")
                return redirect("account:password")
            elif email:
                request.session["email"] = request.POST.get("email")
                otp_code = OTPGenerator()
                otp = otp_code.generate_otp()
                request.session["otp_code"] = otp
                send_mail(
                    'subject',
                    f' ACTIVE CODE : {otp}',
                    'setting.EMAIL_HOST_USER',
                    [request.POST.get("email")],
                    fail_silently=False
                )
                return redirect("account:confirm_email")
            else:
                messages.success(request, 'username or phone number not found ', 'danger')
                return render(request, self.template_class)
        else:
            messages.success(request, 'field email or phone Is Empty ', 'danger')
            return render(request, self.template_class)


class Password(Login):
    template_class = "account/password.html"

    def post(self, request):
        print('hello')
        if request.POST.get("pass"):
            email = request.session.get("username")
            password = request.POST.get("pass")
            user = authenticate(username=email, password=password)
            if user:

                login(request, user)
                if self.next:
                    return redirect(self.next)
                return redirect("core:home")
            else:
                messages.success(request, 'Password is Wrong ', 'danger')
                return render(request, self.template_class)
        else:
            messages.success(request, 'field Password Is Empty ', 'danger')
            return render(request, self.template_class)


class Logout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("core:home")


class SingUp(CreateView):
    template_name = 'account/signup.html'
    # model = User
    form_class = UserCreateForm
    # fields = ['email', 'username', 'phone_number', 'password', 'password2']
    success_url = reverse_lazy('core:home')


class Profile(LoginRequiredMixin, View):
    template_class = "account/profile.html"
    form_class = ProfileForm

    def get(self, request):
        user = request.user
        form = self.form_class(instance=user)
        return render(request, self.template_class, {"form": form})

    def post(self, request):
        user = request.user
        form = self.form_class(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return render(request, self.template_class, {"form": form})
        return render(request, self.template_class, {"form": form})


class ChangePassword(LoginRequiredMixin, View):
    template_class = "account/change_password.html"
    form_class = PasswordForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_class, {"form": form})

    def post(self, request):
        user = request.user
        form = self.form_class(request.POST)
        if form.is_valid():
            result = form.cleaned_data
            if user.check_password(result["password_before"]):
                user.set_password(result["password_new"])
                user.save()
                return redirect("account:profile")
            else:
                messages.success(request, "password is wrong", 'warning')
                return render(request, self.template_class, {"form": form})
        return render(request, self.template_class, {"form": form})


class Signup2(View):
    url = 'account/signup.html'

    def get(self, request):
        form = UserCreateForm()
        return render(request, self.url, {'form': form})

    def post(self, request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # print('username',username)
            # print('password',password)
            # request.session["email"] = form.cleaned_data['email']
            # request.session['custom_user']={
            #     'email':form.cleaned_data['email'],
            #     'username':form.cleaned_data['username'],
            #     'password':form.cleaned_data['password'],
            #     'phone_number':form.cleaned_data['phone_number'],
            # }
            # otp_code=OtpGenerator()
            # otp=otp_code.generate_otp()
            # request.session["otp_code"] =otp
            # send_mail(
            #     'subject',
            #     otp,
            #     'setting.EMAIL_HOST_USER',
            #     [email],
            #     fail_silently=False
            # )
            # user=authenticate(username=username,password=password)
            # if user:
            #     print('salam')
            #     login(request,user)
            messages.success(request, 'register done\n now active account with email (otp code) and login with email ',
                             'success')
            return redirect('account:login')
        return render(request, self.url, {'form': form})


class ConfirmEmail(View):
    template_class = 'account/confirm_email.html'

    def get(self, request):
        return render(request, self.template_class)

    def post(self, request):
        if request.POST.get("otp"):
            email = request.session.get("email")
            next = request.session.get("next")
            otp_user = request.POST.get("otp")
            # print('OTP USER',otp_user)
            # print('OTP EMAIL',otp_email)
            # if otp_user == otp_email:
            #     print('true')
            #     user_object=User.objects.get(email=email)
            #     if user_object:
            #         print('true1')
            #         print(user_object.username)
            #         print(user_object.password)
            #         user_object.is_active=True
            #         user_object.save()
            print(email)
            print(otp_user)
            otp = request.session.get("otp_code")
            print('otp', otp)
            user = authenticate(email=email, otpcode=otp_user, otp_code_send=otp)
            print(user)
            if user:
                print('true2')
                login(request, user)
                if next:
                    return redirect(next)
                return redirect("core:home")
            else:
                messages.success(request, 'otp code is wrong ', 'danger')
                return render(request, self.template_class)
        else:
            messages.success(request, 'field otpcode  Is Empty ', 'danger')
            return render(request, self.template_class)
