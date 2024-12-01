from django.contrib.auth.models import User # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from model.models import (
    RoleModel,
    UserProfileSerializer
)

def create_user_service(self, request):
    """
    Service to register a new user and assign a role.
    """
    data = request.data

    # Check if username already exists
    if User.objects.filter(username=data.get('username')).exists():
        return Response({'detail': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # If password is not provided, set a default
    password = data.get('password', '').strip()
    if not password:
        password = 'Password123'

    # Create the user
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=password
    )

    # Assign role if provided
    role_name = data.get('role', 'Default Role')  # Default Role as fallback
    role, created = RoleModel.objects.get_or_create(name=role_name)
    role.users.add(user)

    serializer = self.get_serializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

def me_service(request) -> Response:
    user = request.user  # Get the current logged-in user (assuming you use JWT or session authentication)
    serializer = UserProfileSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

def assigned_user_role_service(user_id, role_id) -> Response:
    user = User.objects.get(id=user_id)
    role = RoleModel.objects.get(id=role_id)
    user.roles.add(role)
    return Response({"detail": f"Role '{role.name}' assigned to user {user.username}."}, status=status.HTTP_200_OK)