from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from drf_yasg.utils import swagger_auto_schema # type: ignore

# Service
from service.views import register_user_service, login_user_service

# Model
from model.models import REGISTER_REQUEST_BODY, LOGIN_REQUEST_BODY

@swagger_auto_schema(
    method='post',
    request_body=REGISTER_REQUEST_BODY,
    responses={
        201: 'User created successfully',
        400: 'Bad Request',
        500: 'Internal Server Error',
    }
)
@api_view(['POST'])
def register_user(request):
    """
    Controller to register a new user.
    """
    try:
        # Delegating the logic to the service layer
        return register_user_service(request.data)
    except KeyError as e:
        return Response({'detail': f'Missing field: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema(
    method='post',
    request_body=LOGIN_REQUEST_BODY,
    responses={
        200: 'Authentication successful',
        401: 'Invalid credentials',
        500: 'Internal Server Error',
    }
)
@api_view(['POST'])
def login_user(request):
    """
    Controller for user login. Delegates logic to the service layer.
    """
    try:
        return login_user_service(request.data)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)