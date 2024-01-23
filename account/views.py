from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, RedirectView, ListView, DetailView, FormView, CreateView, DeleteView, \
    UpdateView
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q, F
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
        return render(request, self.template_class)

    def post(self, request):
        if request.POST.get("email"):
            email = request.POST.get("email")
            user = CustomUser.objects.filter(Q(username=email) | Q(phone_number=email)).exists()
            email = CustomUser.objects.filter(email=email).exists()
            if user:
                request.session["username"] = request.POST.get("email")
                return redirect("account:password")
            elif email:
                otp_gen = OTPGenerator()
                otp = otp_gen.generate_otp()
                send_mail(
                    "otpcode",
                    otp,
                    'settings.EMAIL_HOST_USER',
                    [request.POST.get("email")],
                    fail_silently=False
                )
                return redirect("account:email")
            else:
                messages.success(request, 'username or phone number not found ', 'danger')
                return render(request, self.template_class)
        else:
            messages.success(request, 'field email or phone Is Empty ', 'danger')
            return render(request, self.template_class)


class Password(Login):
    template_class = "account/password.html"

    def post(self, request):
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


class Email(Password):
    template_class = "account/email.html"


# def email(request):
#     if request.method == "POST":
#         message = request.POST["message"]
#         email = request.POST["email"]
#         name = request.POST["name"]
#         send_mail(
#             name,
#             message,
#             'settings.EMAIL_HOST_USER',
#             [email],
#             fail_silently=False
#         )
#     return render(request, 'account/password.html')


class Logout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("account:login")


class SignUp(View):
    template_name = "account/signup.html"
    form_class = CustomUserCreationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:home")
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:login")
        return render(request, self.template_name, {"form": form})


class Signup2(View):
    url = 'account/signup.html'

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.url, {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print('hello')
            form.save()
            return redirect('core:home')
        return render(request, self.url, {'form': form})
