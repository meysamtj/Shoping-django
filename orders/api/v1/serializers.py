from rest_framework import serializers
from account.models import Address
from orders.models import Order
from product.models import Product


class AddToCartViewSerializer(serializers.Serializer):
    pk = serializers.CharField()
    name = serializers.CharField(max_length=100)
    price = serializers.CharField()
    quantity = serializers.CharField(max_length=9)
    discounted_price = serializers.CharField()


class ProductSerializer(serializers.ModelSerializer):
    total_quantity = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ['name', 'price', 'discount', 'price_discount', 'total_quantity']


class UpdateCartSerializer(serializers.Serializer):
    pk = serializers.CharField()
    name = serializers.CharField(max_length=100)
    price = serializers.IntegerField()
    count = serializers.IntegerField()
    image = serializers.ImageField(allow_null=True)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class SubtitleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('is_deleted', 'is_paid')


class DateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'is_deleted': {'write_only': True},
            'is_paid': {'write_only': True},
        }
