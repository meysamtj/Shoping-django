from rest_framework.response import Response
import datetime
import ast
from product.models import Product
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
import json

CART_COOKIE_ID = 'cart'


class CartApi:
    def __init__(self, request) -> None:
        cart = request.COOKIES.get(CART_COOKIE_ID, None)
        self.request = request
        if not cart:
            self.cart = {}
        else:
            self.cart = ast.literal_eval(cart)

    def __iter__(self):
        product_id = self.cart.keys()
        products = Product.objects.filter(id__in=product_id)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['total_price'] = int(item['price']) * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, name, quantity, product):
        print(self.cart)
        if str(product.id) not in self.cart:
            self.cart[str(product.id)] = {'quantity': 0, 'name': name, 'price': str(product.price_discount)}
        print(self.cart)
        print(product.inventory)
        if self.cart[str(product.id)]['quantity'] + int(quantity) > product.inventory:
            return False
        self.cart[str(product.id)]['quantity'] += int(quantity)

    def get_response(self):
        # for i in self.__iter__():
        #     data = UpdateCartSerializer(i)
        #     if data.is_valid():
        #         name = data.validated_data['name']
        response = Response({CART_COOKIE_ID: 'ok', 'len': self.__len__(), 'total_price': self.get_total_price()})
        expires = datetime.datetime.now() + datetime.timedelta(weeks=100)
        expires_string = expires.strftime("%a, %d-%b-%Y %H:%M:%S")
        response.set_cookie(CART_COOKIE_ID, self.cart, expires=expires_string)
        return response

    def delete(self, pk=None):
        if pk is None:
            response = HttpResponseRedirect('/')
            response.delete_cookie(CART_COOKIE_ID)
            return response
        else:
            response = redirect('orders:cart')
            cart_cookie = self.request.COOKIES.get(CART_COOKIE_ID)
            if cart_cookie:
                cart = json.loads(cart_cookie.replace("'", '"'))
                print('cart',cart)

                if str(pk) in cart:
                    print('hast')
                    del cart[str(pk)]
                cart_cookie = json.dumps(cart)
                response.set_cookie(CART_COOKIE_ID, cart_cookie)
            return response

    def get_total_price(self):
        return sum(int(item['price']) * int(item['quantity']) for item in self.cart.values())
