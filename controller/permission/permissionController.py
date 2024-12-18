from rest_framework import viewsets, status  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from drf_yasg.utils import swagger_auto_schema  # type: ignore
from drf_yasg import openapi  # type: ignore
from rest_framework.decorators import action # type: ignore

from model.models import PERMISSION_REQUEST_BODY, ROLE_PARAMETER
from model.models import PermissionModel, PermissionSerializer
from service.views import (
    list_permissions_service, 
    retrieve_permission_service, 
    update_permission_service,
    update_multiple_permissions_service
)

# Define the 'role' query parameter for Swagger
ROLE_PARAMETER = openapi.Parameter(
    'role', openapi.IN_QUERY, description="Filter permissions by role ID",
    type=openapi.TYPE_INTEGER
)

class PermissionViewSet(viewsets.ModelViewSet):
    """
    Viewset to handle permissions for roles.
    Allows updating existing permissions and viewing them.
    """
    queryset = PermissionModel.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

    # Disable unwanted HTTP methods (DELETE, POST, etc.)
    http_method_names = ['get', 'head', 'options', 'patch', 'put']

    @swagger_auto_schema(
        operation_description="List all permissions. Optionally filter by role.",
        manual_parameters=[ROLE_PARAMETER],
        responses={200: PermissionSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        # Call the service function to handle listing permissions
        response = list_permissions_service(request)
        return response

    @swagger_auto_schema(
        operation_description="Retrieve a permission by ID",
        responses={200: PermissionSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        response = retrieve_permission_service(kwargs['pk'])
        return response

    @swagger_auto_schema(
        operation_description="Update an existing permission",
        request_body=PERMISSION_REQUEST_BODY,
        responses={200: PermissionSerializer}
    )
    def update(self, request, *args, **kwargs):
        """
        Handle the update of a permission, allowing role-based changes.
        """
        permission_id = kwargs.get('pk')
        response = update_permission_service(permission_id, request.data)
        return response
    
    @action(detail=False, methods=['put'], url_path='batch-update')
    @swagger_auto_schema(
        operation_description="Batch update permissions",
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=PERMISSION_REQUEST_BODY
        ),
        responses={200: openapi.Response('Permissions updated successfully')}
    )
    def update_multiple(self, request, *args, **kwargs):
        """
        Handle the update of multiple permissions at once.
        """
        permissions_data = request.data  # This is an array of permission updates
        response = update_multiple_permissions_service(permissions_data)
        return response
