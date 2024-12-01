# roleSerializers.py
from rest_framework import serializers # type: ignore

# Delay the import to avoid circular import issues
def get_role_model():
    from .roleModels import RoleModel  # import here to avoid circular import
    return RoleModel

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_role_model()  # Get the model dynamically
        fields = ['id', 'name']
