from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, RedirectView, ListView, DetailView, FormView, CreateView, DeleteView, \
    UpdateView
from django.contrib.auth import login, authenticate, logout
from .forms import MyLoginForm

class Login(View):
    template_class = "account/login.html"
    form_class =MyLoginForm
    def setup(self, request,  *args, **kwargs) -> None:
        self.next = request.GET.get("next")
        return super().setup(request, *args, **kwargs)

    def get(self,request):
        form = self.form_class
        return render(request, self.template_class, {"form":form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            result = form.cleaned_data
            user = authenticate(username=result["username"], password=result["password"])
            if user:
                login(request,user)
                if self.next:
                    return redirect(self.next)
                return redirect("core:home")
            return render(request, self.template_class, {"form":form})
        return render(request, self.template_class, {"form":form})

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect("account:login")