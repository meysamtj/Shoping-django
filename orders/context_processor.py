from .cart import Cart
from .cart2 import CartApi

def cart(requst):
    return {'cart':CartApi(requst)}