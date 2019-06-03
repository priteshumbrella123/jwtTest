from rest_framework import serializers
from apps.jwtimple.models import Product


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    price = serializers.CharField(required=True)
    brand = serializers.CharField(required=True)
    category_id = serializers.IntegerField(required=True)
    is_active = serializers.BooleanField(default=True)
    is_deleted = serializers.BooleanField(default=False)
    category_name = serializers.SerializerMethodField('capture_category_name')

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "brand",
            "discription",
            "price",
            "category_id",
            "category_name",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at",

        ]

    def capture_category_name(self, obj):

        try:
           return  obj.category.name
        except:
            return None

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.discription = validated_data.get('discription', instance.discription)
        instance.price = validated_data.get('price', instance.price)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.save()
        return instance