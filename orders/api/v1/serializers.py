from rest_framework import serializers


class AddToCartViewSerializer(serializers.Serializer):
    pk = serializers.CharField()
    name = serializers.CharField(max_length=100)
    price = serializers.CharField()
    quantity = serializers.CharField(max_length=9)
    discounted_price = serializers.CharField()


class RemoveFromCartViewSerializer(serializers.Serializer):
    pk = serializers.CharField()


class UpdateCartSerializer(serializers.Serializer):
    pk = serializers.CharField()
    name = serializers.CharField(max_length=100)
    price = serializers.IntegerField()
    count = serializers.IntegerField()
    image = serializers.ImageField(allow_null=True)


class CalculateTotalSerializer(serializers.Serializer):
    total_price = serializers.IntegerField()
    total_count = serializers.IntegerField()


class CalculateDiscountSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=10, allow_blank=True)
    shipping_price = serializers.IntegerField()


class SubmitOrderSerializer(serializers.Serializer):
    shipping_price = serializers.CharField(max_length=100)
    total_price = serializers.CharField(max_length=100)
    address_id = serializers.IntegerField()
