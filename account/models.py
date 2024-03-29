from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.base_user import BaseUserManager
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("The Email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser, BaseModel):
    CUSTOMERUSER_EMPLOYEE = 'employee'
    CUSTOMERUSER_CUSTOMER = 'customer'
    CUSTOMERUSER_MANAGER = 'manager'
    CUSTOMERUSER_STATUS = (
        (CUSTOMERUSER_EMPLOYEE, 'employee'),
        (CUSTOMERUSER_CUSTOMER, 'customer'),
        (CUSTOMERUSER_MANAGER, 'manager')
    )
    GENDER_MEN = "men"
    GENDER_WOMEN = "women"
    GENDER_SELECT = (
        (GENDER_MEN, 'Men'),
        (GENDER_WOMEN, 'Women')
    )
    email = models.EmailField(unique=True, verbose_name=_("email"))
    birth_day = models.DateField(null=True, blank=True, verbose_name=_("birth day"))
    mobile_regex = RegexValidator(regex='^(\+98|0)?9\d{9}$',
                                  message="Phone number must be entered in the format: '+989199999933'.")
    phone_number = models.CharField(validators=[mobile_regex], max_length=20, unique=True, verbose_name=_("phone number"))
    user_type = models.CharField(max_length=8, choices=CUSTOMERUSER_STATUS, default=CUSTOMERUSER_CUSTOMER, verbose_name=_("user type"))
    image = models.ImageField(upload_to='profiles/', blank=True, verbose_name=_("image"))
    national_code = models.CharField(max_length=10, verbose_name=_("national code"))
    gender = models.CharField(max_length=5, choices=GENDER_SELECT, default=GENDER_MEN, verbose_name=_("gender"))
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone_number"]

    def __str__(self):
        return self.email


class Address(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="addreses", verbose_name=_("user"))
    city = models.CharField(max_length=20, verbose_name=_("city"))
    country = models.CharField(max_length=20, default="iran", verbose_name=_("country"))
    street = models.TextField(verbose_name=_("street"))
    state = models.SmallIntegerField(verbose_name=_("state"))

    def __str__(self):
        return f' city --> {self.city} street --> {self.street}'

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Address")