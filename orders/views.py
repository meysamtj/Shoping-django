from django.shortcuts import render,get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, RedirectView, ListView, DetailView, FormView, CreateView, DeleteView, \
    UpdateView
from django.views.generic.list import ListView
from .models import Order, OrderItem
from .cart import Cart
from product.models import Product
from .forms import CartAddForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from account.models import Address 


class CartView(View):
    template_class = 'cart.html'
    def get(self, request):
        cart = Cart(request)
        if request.user.is_authenticated:
            address = Address.objects.filter(user = request.user)
        else:
            address = None
        return render(request, self.template_class,{'cart':cart, 'address': address})


class CartAddView(View):
    def post(self,request,slug):
        cart = Cart(request)
        product = get_object_or_404(Product, slug=slug)
        form=CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product,form.cleaned_data['quantity'])
        return redirect('orders:cart')

class CartRemove(View):
    def setup(self, request, *args, **kwargs) -> None:
        self.next = ''
        if request.GET.get("next"):
            self.next = request.GET.get("next")
            request.session["next"] = self.next
        return super().setup(request, *args, **kwargs)
    def get(self,request,slug):
        cart = Cart(request)
        product = get_object_or_404(Product, slug = slug)
        cart.remove(product)
        return redirect('orders:cart')

class OrderDetailView(LoginRequiredMixin,View):
    temlate_class = 'checkout.html'
    def get(self,request, order_id):
        order = get_object_or_404(Order, id = order_id)
        cart = Cart(request)
        return render(request, self.temlate_class, {'order':order, 'cart':cart} )

class OrderCreateView(LoginRequiredMixin,View):
    def get(self,request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        # order = Order(user=request.user)
        # order.save()
        for item in cart:
            OrderItem.objects.create(order = order,product = item['product'], quantity =item['quantity'])
                                     
            # order_item = OrderItem(order = order,Product = item['product'], quantity =item['quantity'])
            # order_item.save()
                           
        return redirect('orders:order_detail', order.id)
    

class CreateAddress(LoginRequiredMixin,View):
    def post(self,request):
        if request.user.is_authenticated:
            user = request.user
        else:
            return redirect("core:home")
        country = request.POST.get("country")
        city = request.POST.get("city")
        street = request.POST.get("street")
        state = request.POST.get("state")
        Address.objects.create(user = user, country=country, city=city,street=street,state=state)
        return redirect("orders:checkout")
    
class CheckoutView(CartView):
    template_class = "checkout.html"

class CreateOrder(View):
    pass