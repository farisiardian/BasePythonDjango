from rest_framework import viewsets, status # type: ignore
from rest_framework.decorators import action # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework_simplejwt.authentication import JWTAuthentication # type: ignore
from django.contrib.auth.models import User # type: ignore
from drf_yasg.utils import swagger_auto_schema # type: ignore

# Service
from service.views import (
    create_user_service,
    me_service,
    assigned_user_role_service
)

# Model
from model.models import (
    USER_REQUEST_BODY, 
    ASSIGNED_REQUEST_BODY
)
from model.models import RoleModel
from model.models import (
    UserSerializer,
    UserProfileSerializer
)

# Serializers
from model.models import RoleSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD for User Model
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Create User (register) and assign role (if provided)
    @swagger_auto_schema(
        operation_description="Create a new user (register) and assign a role.",
        request_body=USER_REQUEST_BODY,  # Your custom request body schema
        responses={201: "User created successfully", 400: "Validation error"}
    )
    def create(self, request, *args, **kwargs):
        try:
            return create_user_service(self, request)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Custom endpoint for getting details of the currently logged-in user
    @action(detail=False, methods=['get'])
    @swagger_auto_schema(
        operation_description="Get details of the currently logged-in user",
        responses={200: UserProfileSerializer()}
    )
    def me(self, request):
        return me_service(request)

    # Assign a role to the user (Custom action)
    @action(methods=['post'], detail=False, url_path='assign-role')
    @swagger_auto_schema(
        operation_description="Assign a role to the user.",
        request_body=ASSIGNED_REQUEST_BODY,
        responses={200: "Role assigned successfully", 400: "Validation error"}
    )
    def assign_role(self, request):
        user_id = request.data.get('user_id')  # Get user_id from request body
        role_id = request.data.get('role_id')  # Get role_id from request body
        try:
            return assigned_user_role_service(user_id, role_id)
        except RoleModel.DoesNotExist:
            return Response({"detail": "Role not found."}, status=status.HTTP_400_BAD_REQUEST)
