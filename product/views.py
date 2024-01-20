from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView, ListView, DetailView
from .models import Product, Image
from orders.models import OrderItem


# Create your views here.


class Products(ListView):
    template_name = 'product/product.html'
    model = Product  # object Product.objects.filter(id=pk)
    context_object_name = 'products_all'

    def get_queryset(self):
        return Product.objects.filter(category__id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.ten_product_new()
        context["top_cells"] = OrderItem.top_cell_product()
        context["ten_discounts"] = Product.objects.is_discount()
        return context


class DetailProduct(ListView):
    template_name = 'product/detail2.html'
    model = Product  # object Car.objects.filter(id=pk)
    slug_field = 'slug'
    context_object_name = 'product'

    # queryset=Product.objects.get(slug=slug_field)
    def get_queryset(self):
        return Product.objects.get(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images"] = Image.objects.filter(product=self.get_queryset())
        context["relateds"] = Product.objects.filter(category=self.get_queryset().category).exclude(id=self.get_queryset().id)
        return context
