from rest_framework import viewsets, status # type: ignore
from rest_framework.decorators import action # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework_simplejwt.authentication import JWTAuthentication # type: ignore
from django.contrib.auth.models import User # type: ignore
from model.models import UserSerializer # type: ignore
from drf_yasg.utils import swagger_auto_schema # type: ignore

# Service
from service.views import create_user_service

# Model
from model.models import USER_REQUEST_BODY

class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD for User Model
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Override the create method for registering a new user
    @swagger_auto_schema(
        operation_description="Create a new user (register)",
        request_body=USER_REQUEST_BODY,
        responses={201: "User created successfully", 400: "Validation error"}
    )
    def create(self, request, *args, **kwargs):
        try:
            return create_user_service(self, request)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Add a custom endpoint for current user details
    @action(detail=False, methods=['get'])
    @swagger_auto_schema(
        operation_description="Get details of the currently logged-in user",
        responses={200: UserSerializer()}
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
