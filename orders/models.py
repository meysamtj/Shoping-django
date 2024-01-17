from django.db import models
from account.models import CustomUser
from product.models import Product, Discount
from core.models import BaseModel, BaseModelOrder
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Order(BaseModelOrder):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name="orders", null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('is_paid', '-updated_at')

    def __str__(self):
        return f'user -->{self.user} total--> {self.total}'

    # def total_price(self):
    #     return sum(item.get_cost() for item in self.orderitems.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orderitems')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f'OrderItem: {self.id} : {self.product.item_name} X {self.quantity} price:{self.product.price_discount}'

    def get_cost(self):
        return self.product.price_discount * self.quantity

    def clean(self):
        if self.quantity > self.product.inventory:
            raise ValidationError({'quantity': ('مقدار دریافت کالا بیشتر از موجودی می باشد')})
        
    @classmethod
    def top_cell_product(cls):
        orderitems=cls.objects.all()
        list_counter=set([(order_items.counter_cell_product(order_items.product),order_items.product.item_name) for order_items in  orderitems])
        sorted_by_second = sorted(list_counter, key=lambda tup: tup[0], reverse=True)
        return sorted_by_second[:10]
    
    @staticmethod
    def counter_cell_product(product):
        orderitems=OrderItem.objects.filter(product=product)
        sum_cell=sum([item.quantity for item in orderitems])
        return sum_cell 

    

    # def save(self, *args, **kwargs):
    #     self.product.inventory-=self.quantity
    #     self.product.save()
    #     # product = Product.objects.get(pk=self.product.id)
    #     # product.inventory -=self.quantity
    #     # product.save()
    #     super().save(*args, **kwargs)
