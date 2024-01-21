from django.shortcuts import render, redirect
from django.views.generic import TemplateView, RedirectView, ListView, DetailView
from .models import Product, Image, Comment, Like
from orders.models import OrderItem
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.views import View
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.


class Products(ListView):
    template_name = 'product/product(1).html'
    model = Product  # object Product.objects.filter(id=pk)
    context_object_name = 'products_all'
    paginate_by = 6

    def get_queryset(self):
        return [ (product.is_like(self.request.user),product) for product in Product.objects.filter(category__id=self.kwargs['pk']) ] 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.ten_product_new()
        context["top_cells"] = OrderItem.top_cell_product()
        context["ten_discounts"] = Product.objects.is_discount()
        context["len"]= len(self.get_queryset())
        return context


class DetailProduct(ListView):
    template_name = 'product/details.html'
    model = Product  # object Car.objects.filter(id=pk)
    slug_field = 'slug'
    context_object_name = 'product'

    # queryset=Product.objects.get(slug=slug_field)
    def get_queryset(self):
        return Product.objects.get(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images"] = Image.objects.filter(product=self.get_queryset())
        context["relateds"] = Product.objects.filter(category=self.get_queryset().category).exclude(
            id=self.get_queryset().id)
        comments=Comment.objects.select_related('product').filter(product=self.get_queryset(),is_reply=False)
        paginator=Paginator(comments,3)
        page_number=self.request.GET.get("page",1)
        page_objj=paginator.get_page(page_number)
        context["page_obj"]=page_objj
        context['liked']=True if self.get_queryset().is_like(self.request.user) else False 
        return context

class Search(ListView):
    template_name = 'product/product(1).html'
    context_object_name = 'products_all'
    paginate_by = 6

    def get_queryset(self):
        if self.request.GET.get("search"):
            search = self.request.GET.get("search")
            search_query = self.request.GET.get('search')
            search = [ (product.is_like(self.request.user),product) for product in Product.objects.filter(Q(name__icontains=search_query) | Q(category__name__icontains=search_query))]
            return search
        else:
            return [ (product.is_like(self.request.user),product) for product in Product.objects.all() ] 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.ten_product_new()
        context["top_cells"] = OrderItem.top_cell_product()
        context["ten_discounts"] = Product.objects.is_discount()
        context["len"]= len(self.get_queryset())
        return context

class CommentAdd(View):

    def setup(self, request, *args ,**kwargs):
        self.product=Product.objects.get(pk=kwargs['get_id'])
        return super().setup(request, *args, **kwargs)

    def post(self,request,get_id):
        if request.POST['body'] and request.user.is_authenticated:
            comment=Comment(user=request.user,product=self.product,body=request.POST['body'])
            comment.save()
            messages.success(request,'comment add  ','success')
        else :
            messages.success(request,'you are not login or text is empty','danger')
        return redirect('products:detail',self.product.slug)

class LikeAdd(View):

    def setup(self, request, *args, **kwargs):
        self.product=Product.objects.get(pk=kwargs['get_id'])
        return super().setup(request, *args, **kwargs)

    def get(self,request,get_id):
        if self.product.is_like(request.user):
            like=Like(user=request.user,product=self.product)
            like.save()
            messages.success(request,'Like Done  ','success')
        else:
            messages.success(request,'You cannot like once more ','danger')
        return redirect('products:detail',self.product.slug)