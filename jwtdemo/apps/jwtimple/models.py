from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.IntegerField(default=0)
    updated_by = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.name

class User(AbstractUser):
    mobile = models.CharField(max_length=14, null=True)
    password_reset_token = models.CharField(max_length=255,null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE,
                             related_name='rq_role', related_query_name='rqn_role')
    last_login = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.mobile

    @property
    def get_all_module_actions(self):
        user = User.objects.filter(id=self.id,
                                   is_deleted=False,
                                   is_active=True,
                                  ).values_list(
            'role__role_action__module_action__action',flat=True
        )
        return list(user)


class ModuleAction(models.Model):
    action = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.IntegerField(default=0)
    updated_by = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'module_actions'

    def __str__(self):
        return self.action


class RoleModuleAction(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_actions',
                             related_query_name='role_action')
    module_action = models.ForeignKey(ModuleAction, on_delete=models.CASCADE, related_name='rn_module_actions',
                                      related_query_name='rqn_module_action', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.IntegerField(default=0)
    updated_by = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'role_module_actions'


class Category(models.Model):
    name = models.CharField(max_length=150)
    discription = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='rq_category',related_query_name='rqn_category')
    name = models.CharField(max_length=150)
    discription = models.TextField()
    brand  =  models.CharField(max_length= 150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
