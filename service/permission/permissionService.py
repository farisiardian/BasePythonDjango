from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore

from model.models import (
    PermissionModel,
    PermissionSerializer,
    RoleModel
)

def list_permissions_service(request) -> Response:
    # Use the get_queryset method to filter permissions based on the role query parameter
    queryset = get_queryset(request)  # This will automatically apply the filtering logic defined in get_queryset
    serializer = PermissionSerializer(queryset, many=True)
    return Response(serializer.data)

def get_queryset(request):
    role_id = request.query_params.get('role', None)
    if role_id:
        # If the role query parameter is provided, filter by role
        return PermissionModel.objects.filter(role_id=role_id)
    # If no role parameter, return all permissions
    return PermissionModel.objects.all()

def retrieve_permission_service(permission_id) -> Response:
    try:
        permission = PermissionModel.objects.get(id=permission_id)
        serializer = PermissionSerializer(permission)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except PermissionModel.DoesNotExist:
        return Response({"detail": "Permission not found."}, status=status.HTTP_404_NOT_FOUND)

def update_permission_service(permission_id, data) -> Response:
    """
    Service function to handle updating a permission.
    """
    try:
        permission = PermissionModel.objects.get(id=permission_id)

        # Ensure 'role' is being set properly
        role = RoleModel.objects.get(id=data['role'])
        permission.role = role

        # Update 'description' and 'is_permission'
        permission.description = data.get('description', permission.description)
        permission.is_permission = data.get('is_permission', permission.is_permission)  # Update the field here

        permission.save()

        serializer = PermissionSerializer(permission)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except PermissionModel.DoesNotExist:
        return Response({"detail": "Permission not found."}, status=status.HTTP_404_NOT_FOUND)
    except RoleModel.DoesNotExist:
        return Response({"detail": "Role not found."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

def update_multiple_permissions_service(data) -> Response:
    """
    Service function to handle updating multiple permissions.
    """
    try:
        updated_permissions = []

        for permission_data in data:
            permission = PermissionModel.objects.get(id=permission_data['id'])

            # Ensure role exists
            role = RoleModel.objects.get(id=permission_data['role'])
            permission.role = role

            # Update permission fields
            permission.description = permission_data.get('description', permission.description)
            permission.is_permission = permission_data.get('is_permission', permission.is_permission)
            permission.save()

            # Collect updated permissions for response
            updated_permissions.append(permission)

        # Serialize and return the updated permissions
        serializer = PermissionSerializer(updated_permissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except PermissionModel.DoesNotExist:
        return Response({"detail": "Permission not found."}, status=status.HTTP_404_NOT_FOUND)
    except RoleModel.DoesNotExist:
        return Response({"detail": "Role not found."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)