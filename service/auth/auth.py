from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.hashers import make_password # type: ignore
from django.contrib.auth import authenticate # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore

def register_user_service(data):
    """
    Service to register a new user.
    """
    # Check if the username already exists
    if User.objects.filter(username=data['username']).exists():
        return Response({'detail': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user
    user = User.objects.create(
        username=data['username'],
        email=data['email'],
        password=make_password(data['password']),
    )

    # Generate tokens for the new user
    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)

def login_user_service(data):
    """
    Service to handle user login and return JWT tokens.
    """
    username = data.get('username')
    password = data.get('password')

    # Authenticate the user
    user = authenticate(username=username, password=password)

    if user is not None:
        # Generate tokens for the authenticated user
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
