from rest_framework import serializers  # type: ignore

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # Temporarily set to None
        fields = ['id', 'role', 'permission_name', 'description']

    def __init__(self, *args, **kwargs):
        # Lazy import within the serializer's constructor
        from model.models import PermissionModel  # Avoid circular import at the top level
        self.Meta.model = PermissionModel  # Dynamically assign the model
        super().__init__(*args, **kwargs)
