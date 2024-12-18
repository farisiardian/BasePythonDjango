from rest_framework import serializers  # type: ignore
from .permissionModels import PermissionModel

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionModel
        fields = ['id', 'role', 'permission_name', 'description', 'is_permission']
        ref_name = "Permission Serializer For Permission Module"  # Set a unique ref_name
