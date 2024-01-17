from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from core.models import BaseModel, StatusMixin, Basemodeldiss
from account.models import CustomUser
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.utils import timezone
# from orders.models import OrderItem
from django.utils.text import gettext_lazy as _


class Category(BaseModel, StatusMixin):
    category_name = models.CharField(max_length=255, verbose_name=_("category_name"))
    category = models.ForeignKey('self', on_delete=models.CASCADE, related_name="categories",
                                 verbose_name=_("category"), blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, max_length=255, verbose_name=_("slug"))
    image = models.ImageField(upload_to="categories", null=True, blank=True, verbose_name=_("image"))

    class Meta:
        ordering = ("category_name",)
        verbose_name = _("category_name")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.category_name}-{self.id}')
        super().save(*args, **kwargs)


class Product(BaseModel, StatusMixin):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products",
                                 verbose_name=_("category"))
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE, related_name="products", blank=True, null=True,
                                 verbose_name=_("discount"))
    price = models.PositiveIntegerField(verbose_name=_("price"))
    inventory = models.PositiveIntegerField(verbose_name=_("inventory"))
    item_name = models.CharField(max_length=255, verbose_name=_("item name"))
    brand = models.CharField(max_length=255, verbose_name=_("brand"))
    description = models.TextField(verbose_name=_("description"))
    slug = models.SlugField(unique=True, blank=True, max_length=255, verbose_name=_("slug"))
    image = models.ImageField(upload_to="products", verbose_name=_("image"))
    color = models.CharField(max_length=255, default="black", verbose_name=_("color"))
    price_discount = models.PositiveIntegerField(default=0, verbose_name=_("price_discount"))

    class Meta:
        ordering = ("-id",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def clean(self):
        if self.discount:
            if self.discount.type == "number" and self.discount.amount > self.price:
                raise ValidationError({'discount': ('برای تخفیف عددی نباید مقدار  تخفیف بیشتر از مبلغ محصول باشد')})

    def __str__(self):
        return f'name : {self.item_name} | inventory : {self.inventory} '

    def like_count(self):
        return self.likes.count()

    def is_like(self, user):
        like = user.likes.filter(product=self).exists()
        if like:
            return True
        else:
            return False

    # def counter_cell_product(self):
    #     orderitems=OrderItem.objects.filter(product=self)
    #     sum_cell=sum([item.quantity for item in orderitems])
    #     return sum_cell 

    # def top(self):
    #     product = self.objects.all()
    #     list=[(item.counter_cell_product,item.item_name) for item in product]
    #     sort_list = sorted(list, key=lambda x : x[0], reverse=True)
    #     return sort_list[:10]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.item_name}-{self.id}')
        super().save(*args, **kwargs)


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name=_("product"))
    image  = models.ImageField(upload_to="imgproducts", verbose_name=_("image"))

    def __str__(self):
        return self.product.item_name

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")


class Discount(Basemodeldiss):
    TYPE_PERCENT = "percent"
    TYPE_NUMBER = "number"
    TYPE_SELECT = (
        (TYPE_PERCENT, 'PERCENT'),
        (TYPE_NUMBER, 'NUMBER')
    )

    def max_diss_check(value):
        if type == "number" and value != 0.0:
            raise ValidationError(
                ("%(value)s برای تخفیف های درصدی میبایست این مقدار 0.0 باشد"),
                params={"value": value},
            )

    def amount_check(value):
        if type == "percent" and value > 100:
            print("meysam")
            raise ValidationError(
                ("%(value)s برای تخفیف درصدی نباید مقدار درصد بیشتر از 100 باشد"),
                params={"value": value},
            )

    expire = models.DateTimeField(default=timezone.now() + timedelta(days=1, minutes=5), verbose_name=_("expire"))
    type = models.CharField(max_length=10, choices=TYPE_SELECT, default=TYPE_PERCENT, verbose_name=_("type"))
    max_dis = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("max_dis"))
    discount_code = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("discount_code"))
    amount = models.PositiveIntegerField(verbose_name=_("amount"))

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")

    def __str__(self):
        return f'type --> {self.type} amount --> {self.amount}'

    def clean(self):
        if self.type == "percent" and self.amount > 100:
            raise ValidationError({'amount': ('برای تخفیف درصدی نباید مقدار درصد بیشتر از 100 باشد')})
        elif self.type == "number" and self.max_dis:
            raise ValidationError({'max_dis': ('  برای مقادیر عددی این فیلد میبایست خالی باشد')})
        elif self.expire < timezone.now() + timedelta(days=1):
            raise ValidationError({'expire': (' تاریخ انقضا باید حداقل از  فردا شروع گردد')})
        elif self.type == "percent" and self.discount_code:
            raise ValidationError({'discount_code': ('  برای مقادیر درصدی این فیلد میبایست خالی باشد')})


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="likes", verbose_name=_("user"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="likes", verbose_name=_("product"))

    def __str__(self):
        return f'{self.user} liked {self.product.item_name}'

    def clean(self):
        can = Like.objects.filter(user=self.user, product=self.product).exists()
        if can:
            raise ValidationError({'user': (' یک بار با این کاربری لایک انجام شده است')})

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")


class Comment(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments', verbose_name=_("user"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name=_("product"))
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='comments', blank=True, null=True,
                              verbose_name=_("reply"))
    is_reply = models.BooleanField(default=False, verbose_name=_("is reply"))
    body = models.TextField(verbose_name=_("body"))

    class Meta:
        ordering = ("-id",)
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self) -> str:
        return f'{self.user} comment for {self.product.item_name}'
