from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore

from model.models import (
    PermissionModel,
    PermissionSerializer,
    RoleModel,
    PermissionHelperModel
)


def create_permission_service(data) -> Response:
    try:
        # Get the role by ID
        role = RoleModel.objects.get(id=data['role'])

        # Fetch the PermissionHelper by permission_name (key)
        permission_helper = PermissionHelperModel.objects.get(key=data['permission_name'])

        # Create the permission
        permission = PermissionModel.objects.create(
            role=role,
            permission_name=permission_helper.key,  # Use key for permission_name
            description=data.get('description', '')
        )
        serializer = PermissionSerializer(permission)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except RoleModel.DoesNotExist:
        return Response({"detail": "Role not found"}, status=status.HTTP_400_BAD_REQUEST)
    except PermissionHelperModel.DoesNotExist:
        return Response({"detail": "Permission Helper not found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

def list_permissions_service() -> Response:
    permissions = PermissionModel.objects.all()
    serializer = PermissionSerializer(permissions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def retrieve_permission_service(permission_id) -> Response:
    try:
        permission = PermissionModel.objects.get(id=permission_id)
        serializer = PermissionSerializer(permission)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except PermissionModel.DoesNotExist:
        raise Exception("Permission not found")

def update_permission_service(permission_id, data) -> Response:
    try:
        permission = PermissionModel.objects.get(id=permission_id)
        role = RoleModel.objects.get(id=data['role'])

        # Fetch the PermissionHelper by permission_name (key)
        permission_helper = PermissionHelperModel.objects.get(key=data['permission_name'])

        permission.role = role
        permission.permission_name = permission_helper.key  # Use key for permission_name
        permission.description = data.get('description', permission.description)
        permission.save()

        serializer = PermissionSerializer(permission)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except PermissionModel.DoesNotExist:
        return Response({"detail": "Permission not found"}, status=status.HTTP_404_NOT_FOUND)
    except PermissionHelperModel.DoesNotExist:
        return Response({"detail": "Permission Helper not found"}, status=status.HTTP_400_BAD_REQUEST)
    except RoleModel.DoesNotExist:
        return Response({"detail": "Role not found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

def delete_permission_service(permission_id) -> Response:
    try:
        permission = PermissionModel.objects.get(id=permission_id)
        permission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except PermissionModel.DoesNotExist:
        return Response({"detail": "Permission not found"}, status=status.HTTP_404_NOT_FOUND)
