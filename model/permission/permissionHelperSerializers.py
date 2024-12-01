from rest_framework import serializers # type: ignore
from model.models import PermissionHelperModel

class PermissionHelperSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionHelperModel
        fields = ['id', 'key', 'name', 'description']
