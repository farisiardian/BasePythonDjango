from rest_framework import serializers  # type: ignore

# Delay the import to avoid circular import issues
def get_role_model():
    from .roleModels import RoleModel  # import here to avoid circular import
    return RoleModel

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_role_model()  # Get the model dynamically
        fields = ['id', 'name']
        ref_name = "Role Serializer For Role Module"  # Set a unique ref_name
