from rest_framework import serializers
from apps.jwtimple.models import Role
from apps.jwtimple.models import RoleModuleAction


class RoleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    is_active = serializers.BooleanField(default=True)
    is_deleted = serializers.BooleanField(default=False)
    module_action = serializers.SerializerMethodField('capture_module_action')

    class Meta:
        model = Role
        fields = [
            "id",
            "name",
            "module_action",
            "is_active",
            "is_deleted",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",

        ]
    def capture_module_action(self, obj):
        list1 = []
        try:
            x = RoleModuleAction.objects.filter(role_id = obj.id)
            for i in x:
                  list1.append(i.module_action.action)
            print(str(list1))
            return str(list1)

        except:
            return None

    def create(self, validated_data):
        role = Role.objects.create(**validated_data)
        return role

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.save()
        return instance