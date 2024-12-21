from django.conf import settings
from django.db import models
from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
# class CustomUserManager(BaseUserManager):
#     def create_user(self, name, email, is_superuser=False, is_active=True, is_staff=False, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         try:
#             user = self.model(name=name, email=email, is_superuser=is_superuser,
#                               is_active=is_active, is_staff=is_staff, **extra_fields)
#             user.set_password(password)
#             user.save(using=self._db)
#             return user
#         except IntegrityError as e:
#             raise ValueError('User with this email already exists.') from e
#
#
#
#


class UserType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_type')
    user_type = models.CharField(max_length=50, choices=[
        ('hr_staff', 'HR Staff'),
        ('organization_staff', 'Organization Staff'),
    ])


class Role(models.Model):
    name = models.CharField(max_length=100)

# class Permission(models.Model):
#     name = models.CharField(max_length=100)

# class RolePermission(models.Model):
#     role = models.ForeignKey(Role, on_delete=models.CASCADE)
#     permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
#
class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)