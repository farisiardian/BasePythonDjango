from rest_framework import viewsets  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from drf_yasg.utils import swagger_auto_schema  # type: ignore
from rest_framework.response import Response  # type: ignore

from model.models import (
    RoleSerializer,
    ROLE_REQUEST_BODY,
    ROLE_RESPONSE_BODY
)
from service.views import (
    create_role_service,
    retrieve_role_service,
    update_role_service,
    delete_role_service,
    list_roles_service,
)

class RoleViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # Create a new role
    @swagger_auto_schema(
        operation_description="Create a new role",
        request_body=ROLE_REQUEST_BODY,
        responses={201: ROLE_RESPONSE_BODY, 400: "Validation error"}
    )
    def create(self, request, *args, **kwargs):
        response = create_role_service(request.data)
        return response

    # List all roles
    @swagger_auto_schema(
        operation_description="List all roles",
        responses={200: ROLE_RESPONSE_BODY}
    )
    def list(self, request, *args, **kwargs):
        response = list_roles_service()
        return response

    # Retrieve a role by ID
    @swagger_auto_schema(
        operation_description="Retrieve a role by ID",
        responses={200: ROLE_RESPONSE_BODY, 404: "Role not found"}
    )
    def retrieve(self, request, *args, **kwargs):
        role_id = kwargs.get('pk')
        response = retrieve_role_service(role_id)
        return response

    # Update a role
    @swagger_auto_schema(
        operation_description="Update an existing role",
        request_body=ROLE_REQUEST_BODY,
        responses={200: ROLE_RESPONSE_BODY, 400: "Validation error", 404: "Role not found"}
    )
    def update(self, request, *args, **kwargs):
        role_id = kwargs.get('pk')
        response = update_role_service(role_id, request.data)
        return response

    # Delete a role
    @swagger_auto_schema(
        operation_description="Delete a role",
        responses={204: "Role deleted successfully", 404: "Role not found"}
    )
    def destroy(self, request, *args, **kwargs):
        role_id = kwargs.get('pk')
        delete_role_service(role_id)
        return Response(status=204)
