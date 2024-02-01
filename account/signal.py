from django.db.models.signals import post_save,pre_save
from .models import CustomUser
from django.dispatch import receiver
from django.db.models import signals
from django.contrib.auth.models import Group

@receiver(post_save, sender=CustomUser)
def change_user(sender,instance,created, **kwargs):
    if instance.user_type !="customer":
        instance.is_staff =True
        
        if instance.user_type == "manager":
            instance.is_superuser =True
        
        else:
            instance.is_superuser =False
        
        if instance.user_type == "operator":
            group=Group.objects.get(name='operator')
            print('group',group)
            instance.groups.add(Group.objects.get(name='operator'))
            # CustomUser.objects.get(username='masoud').groups.add(Group.objects.get(name='operator'))
            # print(CustomUser.objects.get(username='masoud'))
            # print(instance)
            # # group.user_set.add(kwargs['instance'])
            # print('meysam')
        if instance.user_type == "manage_product":
            group=Group.objects.get(name='manage_product')
            print('group',group)
            instance.groups.add(Group.objects.get(name='manage_product'))
        
        if instance.user_type == "supervisor":
            group=Group.objects.get(name='supervisor')
            print('group',group)
            instance.groups.add(Group.objects.get(name='supervisor'))
    else:
        instance.is_staff =False
        instance.is_superuser =False
        
    
    # for attr in dir(kwargs['instance']):
    #     print(getattr(kwargs['instance'],attr))
    # print(dir(instance))
    post_save.disconnect(change_user, sender=CustomUser)
    instance.save()
    post_save.connect(change_user, sender=CustomUser)


