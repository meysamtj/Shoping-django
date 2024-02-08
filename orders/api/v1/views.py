import datetime

from rest_framework.status import HTTP_406_NOT_ACCEPTABLE
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound

# from user.authentication import JWTAuthentication
from .serializers import *
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
            my_cart.add(name,quantity,product)
            # if cart_info is False:
            #     return Response(status=status.HTTP_400_BAD_REQUEST)
            if my_cart is False:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            response =my_cart.get_response()

            return response
        else:
            return Response({'product': 'not enough'}, status=HTTP_406_NOT_ACCEPTABLE)

