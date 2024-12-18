from rest_framework import serializers # type: ignore
from django.contrib.auth.models import User # type: ignore
from model.role.roleModels import RoleModel
from model.role.roleSerializers import RoleSerializer
from model.permission.permissionModels import PermissionModel
from model.permission.permissionSerializers import PermissionSerializer
from model.user.userModel import UserProfile

class UserSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(
        queryset=RoleModel.objects.all(), write_only=True, required=False
    )
    role_detail = RoleSerializer(source="profile.role", read_only=True)  # Fixed to fetch the role from profile

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'role_detail']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        role = validated_data.pop('role', None)
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
        user.save()

        # Assign role
        if role:
            UserProfile.objects.create(user=user, role=role)
        else:
            UserProfile.objects.create(user=user)

        return user

    def update(self, instance, validated_data):
        role = validated_data.pop('role', None)
        password = validated_data.pop('password', None)

        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        # Update role
        if role:
            profile, created = UserProfile.objects.get_or_create(user=instance)
            profile.role = role
            profile.save()

        return instance
    
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionModel
        fields = ['id', 'role', 'permission_name', 'description', 'is_permission']  # Adjust according to your fields in the PermissionModel

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)  # Include permissions for the role

    class Meta:
        model = RoleModel
        fields = ['id', 'name', 'permissions']

class UserProfileSerializer(serializers.ModelSerializer):
    role = RoleSerializer()  # Include the role with permissions

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'role']  # Include `user` and `role` fields

    def to_representation(self, instance):
        """
        Custom representation to include nested user details if needed.
        """
        representation = super().to_representation(instance)
        representation['user'] = {
            'id': instance.user.id,
            'username': instance.user.username,
            'email': instance.user.email,
        }
        return representation
