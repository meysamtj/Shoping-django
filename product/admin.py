from django.contrib import admin
from .models import Like, Comment, Product, Category,Discount

admin.site.register((Like,Comment,Product,Category,Discount))