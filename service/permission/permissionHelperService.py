from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore

from model.models import (
    PermissionHelperModel,
    PermissionHelperSerializer
)

def list_permissions_helper_service() -> Response:
    permissions = PermissionHelperModel.objects.all()
    serializer = PermissionHelperSerializer(permissions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)