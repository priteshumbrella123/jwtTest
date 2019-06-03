from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
import random
from apps.jwtimple.models import Role


class UserCreateSerializer(serializers.Serializer):
    User = get_user_model()
    first_name = serializers.CharField(max_length=30,required=True)
    last_name = serializers.CharField(max_length=30,required=True)
    email = serializers.CharField(required=True)
    role_id = serializers.IntegerField(required=True)
    mobile = serializers.CharField(required=False)
    password = serializers.CharField(max_length=45, min_length=8, required=True)
    confirm_password = serializers.CharField(max_length=45, min_length=8, required=True)

    def validate_role_id(self, value):
        if not Role.objects.filter(pk=value).exists():
            raise serializers.ValidationError('Role id does not exist.')
        return value

    def validate_mobile(self, value):
        if not value:
            raise serializers.ValidationError('mobile is required field.')
        else:
            try:
                User = get_user_model()
                if not User.objects.filter(mobile=value).exists():
                    if len(str(value)) != 10:
                        raise serializers.ValidationError('mobile number should be of 10 digits')
                    return value
                else:
                    # raise serializers.ValidationError('mobile number is already registered.')
                    return value #For unique mobile number please comment this line uncomment above line
            except Exception as error:
                raise error

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError('email is required field.')
        return value

    def validate_password(self, value):

        if len(value) >= 8 and len(value) <=45:
            return value
        else:
            raise serializers.ValidationError('new password must be between 8 to 45 characters long')

    def validate(self, data):
        """
        Check that password must be equal to confirm password.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("password and confirm password does not match")
        return data

    def create(self, validated_data):
        validated_data['username'] = self.get_unique_username(validated_data['first_name'])
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['is_staff'] = 0
        validated_data['is_superuser'] = 0

        del validated_data['confirm_password']
        user = self.User.objects.create(**validated_data)
        return user

    def get_unique_username(self, first_name):
        username = first_name.upper() + '-' + str(random.randint(10000, 99999))
        if not self.User.objects.filter(username=username).exists():
            return username
        else:
            return self.get_unique_username(first_name)


class UserUpdateSerializer(serializers.Serializer):

    User = get_user_model()
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)
    email = serializers.CharField(required=True)
    role_id = serializers.IntegerField(required=True)
    mobile = serializers.CharField(required=False)
    password = serializers.CharField(max_length=45, min_length=8, required=True)

    def validate_role_id(self, value):
        if not Role.objects.filter(pk=value).exists():
            raise serializers.ValidationError('Role id does not exist.')
        return value

    def validate_mobile(self, value):
        if not value:
            raise serializers.ValidationError('mobile is required field.')
        else:
            try:
                User = get_user_model()
                if not User.objects.filter(mobile=value).exists():
                    if len(str(value)) != 10:
                        raise serializers.ValidationError('mobile number should be of 10 digits')
                    return value
                else:
                    # raise serializers.ValidationError('mobile number is already registered.')
                    return value  # For unique mobile number please comment this line uncomment above line
            except Exception as error:
                raise error

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError('email is required field.')
        return value

    def validate_password(self, value):

        if len(value) >= 8 and len(value) <= 45:
            return value
        else:
            raise serializers.ValidationError('new password must be between 8 to 45 characters long')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.role_id = validated_data.get('role_id', instance.role_id)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.password = validated_data.get('password', instance.password)
        #instance.confirm_password = validated_data.get('confirm_password', instance.confirm_password)
        #del instance.confirm_password
        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField('capture_role_name')
    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'mobile',
            'username',
            'role_name',
            'role_id',
            'password',
            'is_active',
        ]

    def capture_role_name(self, obj):
        try:
           return obj.role.name
        except:
            return None