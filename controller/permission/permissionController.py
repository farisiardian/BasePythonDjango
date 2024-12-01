from rest_framework import viewsets  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from drf_yasg.utils import swagger_auto_schema  # type: ignore
from rest_framework.response import Response  # type: ignore

from model.models import (
    PermissionModel,
    PermissionSerializer,
    PERMISSION_REQUEST_BODY,
    PERMISSION_RESPONSE_BODY
)
from service.views import (
    create_permission_service,
    list_permissions_service,
    retrieve_permission_service,
    update_permission_service,
    delete_permission_service,
)

class PermissionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # Create a new permission
    @swagger_auto_schema(
        operation_description="Create a new permission",
        request_body=PERMISSION_REQUEST_BODY,
        responses={201: PERMISSION_RESPONSE_BODY, 400: "Validation error"}
    )
    def create(self, request, *args, **kwargs):
        response = create_permission_service(request.data)
        return response

    # List all permissions
    @swagger_auto_schema(
        operation_description="List all permissions",
        responses={200: PermissionSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        response = list_permissions_service()
        return response

    # Retrieve a single permission
    @swagger_auto_schema(
        operation_description="Retrieve a permission by ID",
        responses={200: PermissionSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        response = retrieve_permission_service(kwargs['pk'])
        return response

    # Update a permission
    @swagger_auto_schema(
        operation_description="Update an existing permission",
        request_body=PERMISSION_REQUEST_BODY,
        responses={200: PERMISSION_RESPONSE_BODY, 400: "Validation error"}
    )
    def update(self, request, *args, **kwargs):
        response = update_permission_service(kwargs['pk'], request.data)
        return response

    # Delete a permission
    @swagger_auto_schema(
        operation_description="Delete a permission",
        responses={204: "Permission deleted successfully"}
    )
    def destroy(self, request, *args, **kwargs):
        delete_permission_service(kwargs['pk'])
        return Response(status=204)
