from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status

def create_user_service(self, request):
    """
    Service to register a new user.
    """
    data = request.data
    # Check if username already exists
    if User.objects.filter(username=data.get('username')).exists():
        return Response({'detail': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # If password is not provided, set a default
    password = data.get('password', '').strip()
    if not password:
        password = 'Password123'  # Default password if none is provided

    # Create the user (Django automatically hashes the password)
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=password,  # Pass plain password, Django will hash it internally
    )
    serializer = self.get_serializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
