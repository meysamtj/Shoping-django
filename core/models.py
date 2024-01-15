from django.db import models
from datetime import datetime

class LogicalQuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_deleted=True)

    def hard_delete(self):
        return super().delete()


class LogicalManager(models.Manager):

    def get_queryset(self):
        return LogicalQuerySet(self.model).filter(is_deleted=False, is_active=True)

    def archive(self):
        return LogicalQuerySet(self.model)

    def deleted(self):
        return LogicalQuerySet(self.model).filter(is_deleted=True)

class DateBase(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    delete_at = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True
class BaseModel(DateBase):

    is_active = models.BooleanField(default=True)


    objects = LogicalManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super().delete()

    def undelete(self):
        self.is_deleted = False
        self.save()

class StatusMixin:
    @property
    def status(self) -> bool:
        return self.is_active and not self.is_deleted  # noqa
    
class discountQuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_deleted=True)

    def active(self):
        return super().filter(expire__gte= datetime.now()).update(is_active=True)
    
    def deactive(self):
        return super().filter(expire__lte= datetime.now()).update(is_active=False)

    def hard_delete(self):
        return super().delete()

class discountManager(models.Manager):
    def get_queryset(self):
        return discountQuerySet(self.model).filter(is_deleted=False,expire__gte= datetime.now())

    def archive(self):
        return discountQuerySet(self.model)

    def deleted(self):
        return discountQuerySet(self.model).filter(is_deleted=True)


class Basemodeldiss(BaseModel):
        objects = discountManager()
        class Meta:
            abstract = True



class OrderQuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_deleted=True)

    def hard_delete(self):
        return super().delete()


class OrderManager(models.Manager):

    def get_queryset(self):
        return OrderQuerySet(self.model).filter(is_deleted=False)

    def archive(self):
        return OrderQuerySet(self.model)

    def deleted(self):
        return OrderQuerySet(self.model).filter(is_deleted=True)
    
    def paid(self):
        return OrderQuerySet(self.model).filter(is_paid=True,is_deleted=False)
    def no_paid(self):
        return OrderQuerySet(self.model).filter(is_paid=False,is_deleted=False)


class BaseModelOrder(DateBase):
    objects = OrderManager()
    class Meta:
        abstract = True


