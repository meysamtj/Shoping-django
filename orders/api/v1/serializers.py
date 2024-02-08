from rest_framework import serializers


class AddToCartViewSerializer(serializers.Serializer):
    pk = serializers.CharField()
    name = serializers.CharField(max_length=100)
    price = serializers.CharField()
    quantity = serializers.CharField(max_length=9)
    discounted_price = serializers.CharField()

class UpdateCartSerializer(serializers.Serializer):
    pk = serializers.CharField()
    name = serializers.CharField(max_length=100)
    price = serializers.IntegerField()
    count = serializers.IntegerField()
    image = serializers.ImageField(allow_null=True)


