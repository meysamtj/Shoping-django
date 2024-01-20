from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, RedirectView, ListView, DetailView, FormView, CreateView, DeleteView, \
    UpdateView
from django.views.generic.list import ListView
from product.models import Product,Category
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import OrderItem

# Create your views here.


# class Home(View):
#     template = 'core/home.html'

#     def get(self, request):
#         return render(request, self.template)


class Home(ListView):
    
    template_name='core/home.html'
    model=Category
    queryset=Category.objects.all()[:3]
    context_object_name='items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.ten_product_new()
        context["top_cells"] =OrderItem.top_cell_product()
        context["ten_discounts"] =Product.objects.is_discount()
        return context
    
    # def get_context_data(self, **kwargs) :
    #     context = super().get_context_data(**kwargs)
    #     context["form"] = Search()
    #     return context
    # def get_queryset(self):
    #     print('session',self.request.session.get('sabad'))
    #     # print(self.request.GET.get('search'))
    #     if self.request.GET.get('search') :
    #          return Item.objects.select_related('category').filter(name__icontains=self.request.GET.get('search')).order_by('category__create')
    #     return Item.objects.select_related('category').order_by('category__create')
    

class ShowCategorys(ListView):
    
    template_name='core/categories.html'
    model=Category
    context_object_name='items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.ten_product_new()
        context["top_cells"] =OrderItem.top_cell_product()
        context["ten_discounts"] =Product.objects.is_discount()
        return context
    
# class NewProduct(ListView):
#     template_name='core/categories.html'
#     model=Product
#     queryset=Category.objects.all()[:3]
#     context_object_name='products'