from .cart import Cart

def cart(requst):
    return {'cart':Cart(requst)}