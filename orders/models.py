from django.db import models
from account.models import CustomUser
from product.models import Product, Discount
from core.models import BaseModel, BaseModelOrder
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class Order(BaseModelOrder):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders", verbose_name=_("user"))
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name="orders", null=True, blank=True,
                                 verbose_name=_("discount"))
    total = models.PositiveIntegerField(default=0, verbose_name=_("total"))
    is_paid = models.BooleanField(default=False, verbose_name=_("is paid"))
    slug = models.SlugField(unique=False, blank=True, max_length=255, verbose_name=_("slug"))

    class Meta:
        ordering = ('is_paid', '-updated_at')
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f'user -->{self.user} total--> {self.total}'

    def total_price(self):
        return sum(item.get_cost() for item in self.orderitems.all())
    
    def save(self, *args, **kwargs):
        
        # if not self.slug:
        #     counter=1
        #     self.slug = slugify(f'{self.user}')+f'-{counter}'
        #     while Order.objects.filter(slug=self.slug).exists():
        #         counter += 1
        #     self.slug = slugify(f'{self.user}')+f'-{counter}'
        self.slug = slugify(f'{self.user})-{self.id}-{self.total}-{self.is_paid}')
        super().save(*args, **kwargs)    
        

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems', verbose_name=_("order"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orderitems', verbose_name=_("product"))
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name=_("quantity"))
    slug = models.SlugField(unique=True, blank=True, max_length=255, verbose_name=_("slug"))
    def __str__(self):
        return f'{self.product.name} X {self.quantity}'

    def get_cost(self):
        return self.product.price_discount * self.quantity


    def clean(self):
        if self.quantity > self.product.inventory:
            raise ValidationError({'quantity': ('مقدار دریافت کالا بیشتر از موجودی می باشد')})

    @classmethod
    def top_cell_product(cls):
        orderitems = cls.objects.all()
        list_counter = set(
            [(order_items.counter_cell_product(order_items.product), order_items.product) for order_items in
             orderitems])
        sorted_by_second = sorted(list_counter, key=lambda tup: tup[0], reverse=True)
        return sorted_by_second[:10]

    @staticmethod
    def counter_cell_product(product):
        orderitems = OrderItem.objects.filter(product=product)
        sum_cell = sum([item.quantity for item in orderitems])
        return sum_cell

    class Meta:
        verbose_name = _("OrderItem")
        verbose_name_plural = _("OrderItems")
        # def save(self, *args, **kwargs):
    #     self.product.inventory-=self.quantity
    #     self.product.save()
    #     # product = Product.objects.get(pk=self.product.id)
    #     # product.inventory -=self.quantity
    #     # product.save()
    #     super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
        # if not self.slug:
        #     counter=1
        #     self.slug = slugify(f'{self.product.name}')+f'-{counter}'
        #     while OrderItem.objects.filter(slug=self.slug).exists():
        #         counter += 1
        self.slug = slugify(f'{self.product.name})-{self.order.id}-{self.order.id}-{self.quantity}- {self.id}')
        print("meysam")
        super().save(*args, **kwargs)    
        
