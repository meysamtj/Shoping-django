from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name="order_create"),
    path('detail/<int:order_id>/', views.OrderDetailView.as_view(), name="order_detail"),
    path('checkout/', views.CheckoutView.as_view(), name="checkout"),
    path('cart/', views.CartView.as_view(), name="cart"),
    path('cart_add/<slug:slug>/', views.CartAddView.as_view(), name="cart_add"),
    path('cart/remove/<slug:slug>/', views.CartRemove.as_view(), name="remove"),
    path('create_address/', views.CreateAddress.as_view(), name="create_address"),
]
