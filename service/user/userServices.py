from django.contrib.auth.models import User # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from model.models import (
    RoleModel,
    UserProfileSerializer,
    UserProfile
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
    password = data.get('password', 'Password123').strip()

    # Create the user
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=password
    )

    # Assign role if provided
    role_id = data.get('role')  # Role ID
    if role_id:
        try:
            role = RoleModel.objects.get(id=role_id)
            UserProfile.objects.create(user=user, role=role)
        except RoleModel.DoesNotExist:
            return Response({'detail': 'Role not found'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        UserProfile.objects.create(user=user)

    serializer = self.get_serializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def update_user_service(self, request, user_id):
    """
    Service to update user details and their role.
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    # Update user fields
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)

    if 'password' in data:
        user.set_password(data['password'])

    user.save()

    # Update role if provided
    role_id = data.get('role')
    if role_id:
        try:
            role = RoleModel.objects.get(id=role_id)
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = role
            profile.save()
        except RoleModel.DoesNotExist:
            return Response({'detail': 'Role not found'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = self.get_serializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

def me_service(request) -> Response:
    user_profile = UserProfile.objects.get(user=request.user)
    serializer = UserProfileSerializer(user_profile)
    return Response(serializer.data, status=status.HTTP_200_OK)

def assigned_user_role_service(user_id, role_id) -> Response:
    user = User.objects.get(id=user_id)
    role = RoleModel.objects.get(id=role_id)
    user.roles.add(role)
    return Response({"detail": f"Role '{role.name}' assigned to user {user.username}."}, status=status.HTTP_200_OK)