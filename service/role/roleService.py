from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore

from model.models import (
    RoleModel,
    RoleSerializer
)

# Service to create a new role
def create_role_service(data: dict) -> Response:
    try:
        role = RoleModel.objects.create(**data)
        serializer = RoleSerializer(role)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Service to retrieve a role by ID
def retrieve_role_service(role_id: int) -> Response:
    try:
        role = RoleModel.objects.get(id=role_id)
        serializer = RoleSerializer(role)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except RoleModel.DoesNotExist:
        return Response({"detail": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

# Service to update an existing role
def update_role_service(role_id: int, data: dict) -> Response:
    try:
        role = RoleModel.objects.get(id=role_id)
        for key, value in data.items():
            setattr(role, key, value)
        role.save()
        serializer = RoleSerializer(role)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except RoleModel.DoesNotExist:
        return Response({"detail": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

# Service to delete a role
def delete_role_service(role_id: int) -> Response:
    try:
        role = RoleModel.objects.get(id=role_id)
        role.delete()  # Delete role
        return Response(status=status.HTTP_204_NO_CONTENT)
    except RoleModel.DoesNotExist:
        return Response({"detail": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

# Service to list all roles
def list_roles_service() -> Response:
    roles = RoleModel.objects.all()  # Get all roles
    role_data = [{"id": role.id, "name": role.name} for role in roles]
    return Response(role_data, status=status.HTTP_200_OK)
