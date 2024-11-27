from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.hashers import make_password # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore

def create_user_service(self, request):
    """
    Service to register a new user.
    """
    data = request.data
    if User.objects.filter(username=data.get('username')).exists():
        return Response({'detail': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=make_password(data['password']),
    )
    serializer = self.get_serializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)