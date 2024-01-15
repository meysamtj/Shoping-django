from django.db.models.signals import  post_save,pre_delete
from .models import Order,OrderItem
from django.dispatch import receiver


def total(sender,**kwargs):
    if kwargs['created']:
        kwargs['instance'].order.total += kwargs['instance'].get_cost()
        kwargs['instance'].product.inventory -=kwargs['instance'].quantity
        if kwargs['instance'].order.discount:
            if kwargs['instance'].order.discount.type=='number' :
                if kwargs['instance'].order.discount.amount>kwargs['instance'].order.total:
                  kwargs['instance'].order.total=0
                else:
                   kwargs['instance'].order.total -=kwargs['instance'].order.discount.amount
            elif  kwargs['instance'].order.discount.type=='percent' :
               kwargs['instance'].order.total = (kwargs['instance'].order.total* kwargs['instance'].order.discount.amount)/100
        kwargs['instance'].product.save()
        kwargs['instance'].order.save()
post_save.connect(receiver=total,sender=OrderItem)

