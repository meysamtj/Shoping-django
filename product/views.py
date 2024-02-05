from django.shortcuts import render, redirect
from django.views.generic import TemplateView, RedirectView, ListView, DetailView
from .models import Product, Image, Comment, Like, Category
from orders.models import OrderItem
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.views import View
from django.core.paginator import Paginator
from django.contrib import messages
from orders.forms import CartAddForm

# Create your views here.


class Products(ListView):
    template_name = 'product/product.html'
    context_object_name = 'products_all'
    paginate_by = 6

    def get_queryset(self):
        self.category_id = self.kwargs['pk']
        self.categories = Category.objects.all()[:3]
        if self.request.user.is_authenticated:
            return [(product.can_like(self.request.user), product) for product in
                    Product.objects.filter(category__id=self.kwargs['pk'])]
        else:
            return [(False, product) for product in Product.objects.filter(category__id=self.kwargs['pk'])]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.ten_product_new()
        context["top_cells"] = OrderItem.top_cell_product()
        context["ten_discounts"] = Product.objects.is_discount()
        context["len"] = len(self.get_queryset())
        context["category_id"] = self.category_id
        context["items"] = self.categories
        if Category.objects.filter(category__id=self.kwargs['pk']).exists():
            context['category'] = Category.objects.filter(category__id=self.kwargs['pk'])
        return context


class DetailProduct(ListView):
    template_name = 'product/details.html'
    slug_field = 'slug'
    context_object_name = 'product'

    # queryset=Product.objects.get(slug=slug_field)
    def get_queryset(self):
        self.categories = Category.objects.all()[:3]
        product = Product.objects.get(slug=self.kwargs['slug'])
        self.category_id = product.category.id
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images"] = Image.objects.filter(product=self.get_queryset())
        context["relateds"] = Product.objects.filter(category=self.get_queryset().category).exclude(
            id=self.get_queryset().id)
        comments = Comment.objects.select_related('product').filter(product=self.get_queryset(), is_reply=False)
        paginator = Paginator(comments, 3)
        page_number = self.request.GET.get("page", 1)
        page_objj = paginator.get_page(page_number)
        context["page_obj"] = page_objj
        context["category_id"] = self.category_id
        context["items"] = self.categories
        if self.request.user.is_authenticated:
            context['liked'] = True if self.get_queryset().can_like(self.request.user) else False
        else:
            context['liked'] = False
        context['form']= CartAddForm()
        return context


class Search(ListView):
    template_name = 'product/product.html'
    context_object_name = 'products_all'
    paginate_by = 6

    def get_queryset(self):
        self.categories = Category.objects.all()[:3]
        if self.request.GET.get("search"):
            search_query = self.request.GET.get('search')
            if self.request.user.is_authenticated:
                search = [(product.can_like(self.request.user), product) for product in Product.objects.filter(
                    Q(name__icontains=search_query) | Q(category__name__icontains=search_query))]
            else:
                search = [(False, product) for product in Product.objects.filter(
                    Q(name__icontains=search_query) | Q(category__name__icontains=search_query))]
            return search

        else:
            if self.request.user.is_authenticated:
                return [(product.can_like(self.request.user), product) for product in Product.objects.all()]
            else:
                return [(False, product) for product in Product.objects.all()]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.ten_product_new()
        context["top_cells"] = OrderItem.top_cell_product()
        context["ten_discounts"] = Product.objects.is_discount()
        context["len"] = len(self.get_queryset())
        context["items"] = self.categories
        return context

class CommentAdd(View):

    def setup(self, request, *args, **kwargs):
        self.product = Product.objects.get(pk=kwargs['get_id'])
        return super().setup(request, *args, **kwargs)

    def post(self, request, get_id):
        if request.user.is_authenticated:
            if request.POST['body']:
                comment = Comment(user=request.user, product=self.product, body=request.POST['body'])
                comment.save()
                messages.success(request, 'comment add    ', 'success')
            else:
                messages.success(request, 'your text is empty', 'danger')
        else:
            messages.success(request, 'you are not login ', 'danger')
        return redirect('products:detail', self.product.slug)


class LikeAdd(View):

    def setup(self, request, *args, **kwargs):
        self.product = Product.objects.get(pk=kwargs['get_id'])
        self.like = Like.objects.deleted()
        return super().setup(request, *args, **kwargs)

    def get(self, request, get_id):
        if request.user.is_authenticated:

            if self.product.can_like(request.user) and self.product.exist_like(request.user):
                like = Like.objects.get(product=self.product, user=request.user)
                like.undelete()
                messages.success(request, 'Like Done  ', 'success')

            elif self.product.can_like(request.user) and not self.product.exist_like(request.user):
                like = Like(user=request.user, product=self.product)
                like.save()
                messages.success(request, 'Like Done  ', 'success')

            else:
                like = Like.objects.get(product=self.product, user=request.user)
                like.delete()
                # like.is_deleted=True
                # like.save()
                messages.success(request, ' Unlike Done ', 'warning')
        else:
            messages.success(request, 'You are not Login ', 'danger')
        return redirect('products:detail', self.product.slug)
