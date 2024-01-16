from django.db.models.signals import  post_save,pre_delete
from .models import Product
from django.dispatch import receiver


# @receiver(post_save,sender=Order)
def total(sender,**kwargs):
    if kwargs['created']:
        if kwargs['instance'].discount:
           if  kwargs['instance'].discount.type=='number' :
               if kwargs["instance"].price > kwargs["instance"].discount.amount:
                    kwargs['instance'].price_discount =kwargs['instance'].price- kwargs['instance'].discount.amount
           elif  kwargs['instance'].discount.type=='percent' :
                price=(kwargs['instance'].price* kwargs['instance'].discount.amount)/100
                if kwargs['instance'].discount.max_dis and price > kwargs['instance'].discount.max_dis :
                    kwargs['instance'].price_discount = kwargs['instance'].price-kwargs['instance'].discount.max_dis
                else:
                    kwargs['instance'].price_discount = price 
           else :
                kwargs['instance'].price_discount=kwargs['instance'].price
        kwargs['instance'].save()
post_save.connect(receiver=total,sender=Product)
