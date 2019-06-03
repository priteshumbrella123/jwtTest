from rest_framework import serializers
from apps.jwtimple.models import ModuleAction,RoleModuleAction


class ModuleActionSerializer(serializers.ModelSerializer):

    is_active = serializers.BooleanField(default=True)
    is_deleted = serializers.BooleanField(default=False)

    class Meta:
        model = ModuleAction
        fields = [
                'id',
                'action',
                'is_active',
                'is_deleted',
                'created_by',
                'updated_by',
                'created_at',
                'updated_at'
        ]

    def create(self, validated_data):
        module_action = ModuleAction.objects.create(**validated_data)
        return module_action

    def update(self, instance, validated_data):
        instance.action = validated_data.get('action', instance.action)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.save()
        return instance


class RoleModuleActionSerializer(serializers.ModelSerializer):
    role_id = serializers.IntegerField(required=True)
    module_action_id = serializers.ListField(required=True)

    class Meta:
        model = RoleModuleAction
        fields = [
            'id',
            'role_id',
            'module_action_id',
            'is_active',
            'is_deleted',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        message = "Added"
        if RoleModuleAction.objects.filter(role_id=validated_data['role_id']).count()>0:
            message = "Updated"
        RoleModuleAction.objects.filter(role_id=validated_data['role_id']).delete()
        for module_action_id in validated_data['module_action_id']:
            RoleModuleAction.objects.create(role_id=validated_data['role_id'],
                                            module_action_id=module_action_id,
                                            created_by=validated_data['created_by'])
        instance = RoleModuleAction()
        return {"instance":instance, "message":message}