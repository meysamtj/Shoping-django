from django.db import models
from account.models import CustomUser
from product.models import Product, Discount
from core.models import BaseModel
from django.utils.text import slugify

class Order(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete= models.CASCADE, related_name = "orders")
    discount = models.ForeignKey(Discount, on_delete= models.CASCADE, related_name = "orders")
    total = models.PositiveIntegerField()
    is_paid = models.BooleanField(default=False)
    def __str__(self):
        return f'user -->{self.user} total order--> {self.total}'

    

class OrderItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete= models.CASCADE, related_name = "orderitems")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'OrderItem: {self.id} : {self.product} X {self.quantity} (price:{self.price}'