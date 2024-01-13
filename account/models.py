from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.core.validators import RegexValidator
from django.contrib.auth.base_user import BaseUserManager

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
    
class CustomUser(AbstractUser):
    CUSTOMERUSER_EMPLOYEE = 'employee'
    CUSTOMERUSER_CUSTOMER = 'customer'
    CUSTOMERUSER_MANAGER = 'manager'
    CUSTOMERUSER_STATUS = (
        (CUSTOMERUSER_EMPLOYEE,'employee'),
        (CUSTOMERUSER_CUSTOMER,'customer'),
        (CUSTOMERUSER_MANAGER,'manager')
    )
    GENDER_MEN = "men"
    GENDER_WOMEN = "women"
    GENDER_SELECT = (
        (GENDER_MEN,'Men'),
        (GENDER_WOMEN,'Women')
    )
    email = models.EmailField(unique = True)
    birth_day = models.DateField(null=True, blank=True)
    mobile_regex = RegexValidator(regex='^(\+98|0)?9\d{9}$', message="Phone number must be entered in the format: '+989199999933'.")
    phone_number = models.CharField(validators=[mobile_regex], max_length=20, unique=True)
    user_type = models.CharField(max_length=8,choices=CUSTOMERUSER_STATUS, default=CUSTOMERUSER_CUSTOMER)
    image = models.ImageField(upload_to='profiles/', blank=True)
    national_code = models.CharField(max_length=10)
    gender = models.CharField(max_length=5,choices=GENDER_SELECT, default=GENDER_MEN)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone_number"]

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name = "addreses")
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    street = models.TextField()
    state = models.SmallIntegerField()
    
    def __str__(self):
        return f' city --> {self.city} street --> {self.street}'

class Otp_code(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name = "users")
    code = models.TextField()

    def __str__(self):
        return f' code --> {self.code}'

