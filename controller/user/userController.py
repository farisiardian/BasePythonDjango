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
    assigned_user_role_service,
    update_user_service
)

# Model
from model.models import (
    USER_REQUEST_BODY, 
    ASSIGNED_REQUEST_BODY,
    USER_UPDATE_REQUEST_BODY
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

    @swagger_auto_schema(
        operation_description="Retrieve all users along with their roles.",
        responses={200: UserSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        # Use 'profile__role' for prefetching the related role
        users = self.queryset.prefetch_related('profile__role')  # Fetch related profile and role
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Retrieve a specific user along with their role.",
        responses={200: UserSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        try:
            # Use 'profile__role' for prefetching the related role
            user = self.queryset.prefetch_related('profile__role').get(id=user_id)
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

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
    
    # Create User (register) and assign role (if provided)
    @swagger_auto_schema(
        operation_description="Update an existing user and assign a role.",
        request_body=USER_UPDATE_REQUEST_BODY,  # Request body for updating user details and role
        responses={200: "User updated successfully", 400: "Validation error"}
    )
    def update(self, request, *args, **kwargs):
        """Update an existing user and their role."""
        user_id = kwargs.get('pk')  # Get the user's ID from the URL
        return update_user_service(self, request, user_id)
    
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
