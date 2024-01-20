from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    path('<int:pk>/',views.Products.as_view(),name='product'),
    path('detail/<slug:slug>/',views.DetailProduct.as_view(),name='detail'),
]