from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.base_user import BaseUserManager
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from .manager import CustomUserManager




class CustomUser(AbstractUser, BaseModel):
    CUSTOMERUSER_EMPLOYEE = 'employee'
    CUSTOMERUSER_CUSTOMER = 'customer'
    CUSTOMERUSER_MANAGER = 'manager'
    CUSTOMERUSER_SUPERVIZOR = 'supervisor'
    CUSTOMERUSER_STATUS = (
        (CUSTOMERUSER_EMPLOYEE, 'employee'),
        (CUSTOMERUSER_CUSTOMER, 'customer'),
        (CUSTOMERUSER_MANAGER, 'manager'),
        (CUSTOMERUSER_SUPERVIZOR, 'supervisor')
    )
    GENDER_MEN = "men"
    GENDER_WOMEN = "women"
    GENDER_SELECT = (
        (GENDER_MEN, 'Men'),
        (GENDER_WOMEN, 'Women')
    )
    email = models.EmailField(unique=True, verbose_name=_("email"))
    birth_day = models.DateField(null=True, blank=True, verbose_name=_("birth day"),
                                 help_text= "بین تاریخ ها را با - پر نمایید.")
    mobile_regex = RegexValidator(regex='^(\+98|0)?9\d{9}$',
                                  message="Phone number must be entered in the format: '+989199999933'.",
                                  )
    is_active = models.BooleanField(default=False, verbose_name=_("is_active"))
    phone_number = models.CharField(validators=[mobile_regex], max_length=20, unique=True, verbose_name=_("phone number"))
    user_type = models.CharField(max_length=10, choices=CUSTOMERUSER_STATUS, default=CUSTOMERUSER_CUSTOMER, verbose_name=_("user type"))
    image = models.ImageField(upload_to='profiles/', blank=True, verbose_name=_("image"))
    national_code = models.PositiveSmallIntegerField( verbose_name=_("national code"),blank=True,null=True)
    gender = models.CharField(max_length=5, choices=GENDER_SELECT, default=GENDER_MEN, verbose_name=_("gender"))
    objects = CustomUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone_number"]

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