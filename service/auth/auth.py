import jwt
from django.conf import settings
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

    # Create the user with plain password (will be hashed automatically)
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],  # This is plain text, Django will hash it
    )

    # Generate JWT tokens for the new user
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

def decode_jwt(token):
    """
    Decode the JWT token using HS256 algorithm.
    """
    try:
        # Decoding the token using the correct algorithm
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return Response({'detail': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.DecodeError:
        return Response({'detail': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)