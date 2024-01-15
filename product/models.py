from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from core.models import BaseModel, StatusMixin, Basemodeldiss
from account.models import CustomUser
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.utils import timezone


class Category(BaseModel, StatusMixin):
    category_name = models.CharField(max_length=255)
    category = models.ForeignKey('self', on_delete=models.CASCADE, related_name="categories", blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    image = models.ImageField(upload_to="categories", null=True, blank=True)

    class Meta:
        ordering = ("category_name",)
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)


class Product(BaseModel, StatusMixin):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE, related_name="products", blank=True, null=True)
    price = models.PositiveIntegerField()
    inventory = models.PositiveIntegerField()
    item_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    image = models.ImageField(upload_to="products")
    color = models.CharField(max_length=255, default="black")
    price_discount = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("-id",)

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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.item_name}')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("home:detail", args=[self.slug])


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = image = models.ImageField(upload_to="imgproducts")

    def __str__(self):
        return self.product.item_name


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

    expire = models.DateTimeField(default=timezone.now() + timedelta(days=1, minutes=5))
    type = models.CharField(max_length=10, choices=TYPE_SELECT, default=TYPE_PERCENT)
    max_dis = models.PositiveIntegerField(null=True, blank=True)
    discount_code = models.CharField(max_length=20, null=True, blank=True)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f'type --> {self.type} amount --> {self.amount}'

    def clean(self):
        if self.type == "percent" and self.amount > 100:
            raise ValidationError({'amount': ('برای تخفیف درصدی نباید مقدار درصد بیشتر از 100 باشد')})
        elif self.type == "number" and self.max_dis:
            raise ValidationError({'max_dis': ('  برای مقادیر عددی این فیلد میبایست خالی باشد')})
        elif self.expire < timezone.now() + timedelta(days=1):
            raise ValidationError({'expire': (' تاریخ انقضا باید حداقل از  فردا شروع گردد')})


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="likes")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f'{self.user} liked {self.product}'

    def clean(self):
        can = Like.objects.filter(user=self.user, product=self.product).exists()
        if can:
            raise ValidationError({'user': (' یک بار با این کاربری لایک انجام شده است')})


class Comment(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField()

    class Meta:
        ordering = ("-id",)

    def __str__(self) -> str:
        return f'{self.user.username} comment for {self.product.item_name}'
