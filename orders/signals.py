from django.db.models.signals import post_save, pre_delete, pre_save
from .models import Order, OrderItem
from django.dispatch import receiver
from django.db.models import signals

x = 0


@receiver(post_save, sender=OrderItem)
def total_new(sender, **kwargs):
    # if kwargs['created']:
    kwargs['instance'].order.total = 0
    kwargs['instance'].order.total += kwargs['instance'].get_cost()
    # kwargs['instance'].product.inventory -= kwargs['instance'].quantity

    post_save.disconnect(total_new, sender=OrderItem)
    kwargs['instance'].product.save()
    kwargs['instance'].order.save()
    post_save.connect(total_new, sender=OrderItem)


# post_save.connect(receiver=total, sender=OrderItem)
@receiver(post_save, sender=Order)
def total_order(sender, **kwargs):
    # if kwargs['created']:
    kwargs['instance'].total = 0
    kwargs['instance'].total = kwargs['instance'].total_price()
    if kwargs['instance'].discount:
        if kwargs['instance'].discount.type == 'number':
            if kwargs['instance'].discount.amount > kwargs['instance'].total:
                kwargs['instance'].total = 0
            else:
                kwargs['instance'].total -= kwargs['instance'].discount.amount
        elif kwargs['instance'].discount.type == 'percent':
            kwargs['instance'].total = kwargs['instance'].total - (kwargs['instance'].total * kwargs[
                'instance'].discount.amount) / 100

    post_save.disconnect(total_order, sender=Order)
    kwargs['instance'].save()
    post_save.connect(total_order, sender=Order)


@receiver(pre_save, sender=OrderItem)
def counter_quantity(sender, instance, **kwargs):
    if instance.pk:
        previous_instance = sender.objects.get(pk=instance.pk)
        instance.product.inventory -= (instance.quantity - previous_instance.quantity)
    else:
        instance.product.inventory -= instance.quantity
    instance.product.save()
