from rest_framework.viewsets import ReadOnlyModelViewSet  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from drf_yasg.utils import swagger_auto_schema  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore

from model.models import PermissionHelperModel, PermissionHelperSerializer
from service.views import list_permissions_helper_service

class PermissionHelperViewSet(ReadOnlyModelViewSet):
    """
    API endpoint for reading predefined permissions.
    """
    permission_classes = [IsAuthenticated]

    # List all permissions
    @swagger_auto_schema(
        operation_description="List all permissions",
        responses={200: PermissionHelperSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        response = list_permissions_helper_service()
        return response

    # Retrieve a single permission by ID
    @swagger_auto_schema(
        operation_description="Retrieve a permission by ID",
        responses={200: PermissionHelperSerializer, 404: "Not found"}
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            permission = PermissionHelperModel.objects.get(pk=kwargs['pk'])
            serializer = PermissionHelperSerializer(permission)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PermissionHelperModel.DoesNotExist:
            return Response({"detail": "Permission not found"}, status=status.HTTP_404_NOT_FOUND)
