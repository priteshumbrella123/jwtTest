from rest_framework import serializers
from apps.jwtimple.models import Category


class CategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "is_active",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        print("##%%")
        print(validated_data)
        category = Category.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.discription = validated_data.get('discription', instance.discription)
        instance.save()
        return instance