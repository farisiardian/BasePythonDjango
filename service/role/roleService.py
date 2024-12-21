from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.generics import get_object_or_404 # type: ignore
from rest_framework.exceptions import ValidationError # type: ignore
from django.db import transaction # type: ignore
from django.db import IntegrityError # type: ignore
from controller.views import CustomPageNumberPagination
from model.models import (
    RoleModel, 
    RoleSerializer,
    PermissionModel,
    PERMISSIONS
)


# Create a new role and assign permissions
def create_role_service(data: dict) -> Response:
    serializer = RoleSerializer(data=data)
    if serializer.is_valid():
        with transaction.atomic():
            # Save the role
            role = serializer.save()

            # Assign permissions to the role
            for permission in PERMISSIONS:
                PermissionModel.objects.create(
                    role=role,
                    permission_name=permission["permission_name"],
                    description=permission["description"],
                    is_permission=(role.id == 1)  # Enable by default for admin role
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve a role by ID
def retrieve_role_service(role_id: int) -> Response:
    role = get_object_or_404(RoleModel, id=role_id)
    serializer = RoleSerializer(role)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Update an existing role
def update_role_service(role_id: int, data: dict) -> Response:
    role = get_object_or_404(RoleModel, id=role_id)
    serializer = RoleSerializer(role, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete a role
def delete_role_service(role_id: int) -> Response:
    role = get_object_or_404(RoleModel, id=role_id)
    role.delete()
    return Response({"detail": "Role deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# List all roles
def list_roles_service(request) -> Response:
    roles = RoleModel.objects.all()  # Get all roles

    # Paginate the queryset if pagination class is set
    paginator = CustomPageNumberPagination()
    page = paginator.paginate_queryset(roles, request)  # Apply pagination to the roles

    if page is not None:
        # If paginated, serialize the page and return paginated response
        serializer = RoleSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    # If no pagination is needed, return all data
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
