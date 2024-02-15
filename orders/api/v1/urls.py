from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import *
app_name = "api"
urlpatterns = [
    path("add_to_cart/", AddToCartView.as_view(), name="Add to cart"),
    path("plus_to_cart/", PlusToCart.as_view(), name="plus to cart"),
    path("remove_from_cart/", RemoveOfCart.as_view(), name="remove from cart"),
    # path("address/", ShowAddress.as_view(), name="address"),
    path("order/", ShowOrder.as_view(), name="order"),
    # path("subtitle/order", Showsuborder.as_view(), name="subtitle"),
    # path("shopping-cart/", CartItemListView.as_view(), name="shopping cart"),
    path("address/", ShowAddress.as_view(), name="address"),
    path("subtitle/order", SubtitleOrder.as_view(), name="subtitle_order"),
    path("date/order", DateOrder.as_view(), name="date_order"),
    path("order/items/<int:get_id>", OrderItems.as_view(), name="order_items"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)