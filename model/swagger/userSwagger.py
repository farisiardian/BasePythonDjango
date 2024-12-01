from drf_yasg import openapi # type: ignore

USERNAME_FIELD = openapi.Schema(type=openapi.TYPE_STRING, description="Username")
EMAIL_FIELD = openapi.Schema(type=openapi.TYPE_STRING, description="Email address")
PASSWORD_FIELD = openapi.Schema(type=openapi.TYPE_STRING, description="Password")
USER_ID_FIELD = openapi.Schema(type=openapi.TYPE_NUMBER, description="User Id")
ROLE_ID_FIELD = openapi.Schema(type=openapi.TYPE_NUMBER, description="Role Id")

USER_REQUEST_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': USERNAME_FIELD,
        'email': EMAIL_FIELD,
        'password': PASSWORD_FIELD,
    },
    required=['username', 'email', 'password'],
)

ASSIGNED_REQUEST_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'user_id': USERNAME_FIELD,
        'role_id': EMAIL_FIELD,
    },
    required=['username', 'email', 'password'],
)