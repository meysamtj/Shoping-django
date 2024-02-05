from product.models import Product

CART_SESSION_ID= 'cart'

class Cart:
    def __init__(self, request) :
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart =self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_slugs = self.cart.keys()
        products = Product.objects.filter(slug__in = product_slugs)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.slug)]['product'] = product

        for item in cart.values():
            item['total_price'] = int(item['price']) * item['quantity']
            yield item
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self,product,quantity):
        product_slug = str(product.slug)
        if product_slug not in self.cart:
            self.cart[product_slug] = {'quantity':0, 'price':str(product.price_discount)}
        if self.cart[product_slug]['quantity'] +int(quantity) > product.inventory:
            return False
        self.cart[product_slug]['quantity'] +=int(quantity)
        self.save()
    def remove(self,product):
        product_slug = str(product.slug)
        if product_slug in self.cart:
            del self.cart[product_slug]
            self.save()

    def save(self):
        self.session.modified = True
    
    def get_total_price(self):
        return sum(int(item['price'])* int(item['quantity']) for item in self.cart.values())