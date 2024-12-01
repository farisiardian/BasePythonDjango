from rest_framework import serializers # type: ignore
from django.contrib.auth.models import User # type: ignore
from model.role.roleModels import RoleModel
from model.role.roleSerializers import RoleSerializer
from model.permission.permissionSerializers import PermissionSerializer

class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'roles']

class UserRoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)  # Serialize permissions for each role

    class Meta:
        model = RoleModel
        fields = ['id', 'name', 'permissions']

class UserProfileSerializer(serializers.ModelSerializer):
    roles = UserRoleSerializer(many=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'roles']