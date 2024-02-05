from django.db.models.signals import post_save
from .models import CustomUser
from django.dispatch import receiver
from django.db.models import signals


@receiver(post_save, sender=CustomUser)
def change_user(sender, **kwargs):
    if kwargs['instance'].user_type !="customer":
        kwargs['instance'].is_staff =True
        if kwargs['instance'].user_type == "manager":
            kwargs['instance'].is_superuser =True
        else:
            kwargs['instance'].is_superuser =False
    else:
        kwargs['instance'].is_staff =False
        kwargs['instance'].is_superuser =False
    post_save.disconnect(change_user, sender=CustomUser)
    kwargs['instance'].save()
    post_save.connect(change_user, sender=CustomUser)
