import datetime

from rest_framework.status import HTTP_406_NOT_ACCEPTABLE
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
# from user.authentication import JWTAuthentication
from .serializers import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
# from ...models import DiscountCoupon, Cart, Order
# from user.models import User
# from core.views import BasicViewMixin
from product.models import Product
from orders.cart import Cart
from orders.cart2 import CartApi
from rest_framework import status


class AddToCartView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = AddToCartViewSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        pk = serializer.validated_data.get('pk')
        name = serializer.validated_data.get('name')
        price = serializer.validated_data.get('price')
        quantity = serializer.validated_data.get('quantity')
        product = Product.objects.get(pk=pk)
        # cart = request.COOKIES.get('cart', None)
        my_cart = CartApi(request)
        if product.inventory > 0:
            # cart2 = Cart(request)
            # cart_info = cart2.add(product, quantity)
            my_cart2 = my_cart.add(name, quantity, product)
            # if cart_info is False:
            #     return Response(status=status.HTTP_400_BAD_REQUEST)
            if my_cart2 is False:
                print('true')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            response = my_cart.get_response_price(product.id)

            return response
        else:
            return Response({'product': 'not enough'}, status=HTTP_406_NOT_ACCEPTABLE)


# class ShowAddress(APIView):
#     serializer_class = AddressSerializer
#
#     def get(self, request):
#         if request.user.is_authenticated:
#             address = Address.objects.filter(user=request.user)
#             serializer = self.serializer_class(instance=address, many=True)
#             context = {'address_data': serializer.data}
#             return TemplateResponse(request, 'account/address.html', context, status=status.HTTP_200_OK)
#         else:
#             return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)


class ShowOrder(APIView):
    serializer_class = OrderSerializer

    def get(self, request):
        if request.user.is_authenticated:
            order = Order.objects.filter(user=request.user)
            serializer = self.serializer_class(instance=order, many=True)
            context = {'object_list': serializer.data}
            return TemplateResponse(request, 'date_order.html', context, status=status.HTTP_200_OK)
        else:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)


class Showsuborder(APIView):
    serializer_class = OrderSerializer

    def get(self, request):
        if request.user.is_authenticated:
            order = Order.objects.filter(user=request.user)
            serializer = self.serializer_class(instance=order, many=True)
            context = {'object_list': serializer.data}
            return TemplateResponse(request, 'subtitle_order.html', context, status=status.HTTP_200_OK)
        else:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)


class CartItemListView(APIView):
    def get(self, request):
        cart_items = Product.objects.all()
        my_cart = CartApi(request)
        serializer = ProductSerializer(my_cart, many=True)
        return Response(my_cart.get_response())


class PlusToCart(AddToCartView):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        pk = serializer.validated_data.get('pk')
        name = serializer.validated_data.get('name')
        price = serializer.validated_data.get('price')
        quantity = serializer.validated_data.get('quantity')
        product = Product.objects.get(pk=pk)
        # cart = request.COOKIES.get('cart', None)
        my_cart = CartApi(request)
        if product.inventory > 0:
            # cart2 = Cart(request)
            # cart_info = cart2.add(product, quantity)
            my_cart.add(name, quantity, product)
            # if cart_info is False:
            #     return Response(status=status.HTTP_400_BAD_REQUEST)
            if my_cart is False:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            response = my_cart.get_response_price(str(product.id))
            print(response)
            return response
        else:
            return Response({'product': 'not enough'}, status=HTTP_406_NOT_ACCEPTABLE)


class RemoveOfCart(AddToCartView):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        pk = serializer.validated_data.get('pk')
        name = serializer.validated_data.get('name')
        price = serializer.validated_data.get('price')
        quantity = serializer.validated_data.get('quantity')
        product = Product.objects.get(pk=pk)
        # cart = request.COOKIES.get('cart', None)
        my_cart = CartApi(request)
        if product.inventory > 0:
            # cart2 = Cart(request)
            # cart_info = cart2.add(product, quantity)
            my_cart.remove(quantity, product)
            # if cart_info is False:
            #     return Response(status=status.HTTP_400_BAD_REQUEST)
            if my_cart is False:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            response = my_cart.get_response_price(str(product.id))
            print(response)
            return response
        else:
            return Response({'product': 'not enough'}, status=HTTP_406_NOT_ACCEPTABLE)

class ShowAddress(APIView):

    def get(self, request):
        address_list = Address.objects.filter(user=request.user)
        paginator = Paginator(address_list, 10)

        page = request.GET.get('page')
        try:
            addresses = paginator.page(page)
        except PageNotAnInteger:
            addresses = paginator.page(1)
        except EmptyPage:
            addresses = paginator.page(paginator.num_pages)

        serializer_data = AddressSerializer(instance=addresses, many=True)

        context = {
            'object_list': serializer_data.data,
            'addresses': addresses
        }
        return TemplateResponse(request, 'account/address.html', context, status=status.HTTP_200_OK)

    # return TemplateResponse(request, 'account/address.html', context)


class SubtitleOrder(APIView):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)

        paginator = Paginator(orders, 10)

        page = request.GET.get('page')
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)

        serializer_data = SubtitleOrderSerializer(instance=orders, many=True)
        context = {
            'object_list': serializer_data.data,
            'page_obj': orders
        }
        return TemplateResponse(request, 'subtitle_order.html', context, status=status.HTTP_200_OK)


class DateOrder(APIView):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)

        paginator = Paginator(orders, 10)

        page = request.GET.get('page')
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)

        serializer_data = DateOrderSerializer(instance=orders, many=True)
        context = {
            'object_list': serializer_data.data,
            'page_obj': orders
        }
        return TemplateResponse(request, 'date_order.html', context, status=status.HTTP_200_OK)


class OrderItems(APIView):
    def get(self, request, get_id):
        products = Product.objects.prefetch_related('orderitems').filter(orderitems__order__id=get_id)
        products_with_quantity = products.annotate(total_quantity=Sum('orderitems__quantity'))
        print(products_with_quantity)
        paginator = Paginator(products_with_quantity, 10)

        page = request.GET.get('page')
        try:
            products_with_quantity = paginator.page(page)
        except PageNotAnInteger:
            products_with_quantity = paginator.page(1)
        except EmptyPage:
            products_with_quantity = paginator.page(paginator.num_pages)

        serializer_data = ProductSerializer(instance=products_with_quantity, many=True)
        print(serializer_data.data)
        context = {
            'object_list': serializer_data.data,
            'page_obj': products_with_quantity
        }
        return TemplateResponse(request, 'order_item.html', context, status=status.HTTP_200_OK)