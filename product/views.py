from django.shortcuts import render
from django.views import View


class Home(View):
    template_name = ""

    def get(self, request):
        return render(request, self.template_name)
