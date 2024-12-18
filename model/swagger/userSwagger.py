from drf_yasg import openapi  # type: ignore

USERNAME_FIELD = openapi.Schema(type=openapi.TYPE_STRING, description="Username")
EMAIL_FIELD = openapi.Schema(type=openapi.TYPE_STRING, description="Email address")
PASSWORD_FIELD = openapi.Schema(type=openapi.TYPE_STRING, description="Password")
ROLE_ID_FIELD = openapi.Schema(type=openapi.TYPE_NUMBER, description="Role Id")

USER_REQUEST_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': USERNAME_FIELD,
        'email': EMAIL_FIELD,
        'password': PASSWORD_FIELD,
        'role': ROLE_ID_FIELD,  # Optional field for role assignment
    },
    required=['username', 'email', 'password'],
)

USER_UPDATE_REQUEST_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': USERNAME_FIELD,
        'email': EMAIL_FIELD,
        'password': PASSWORD_FIELD,
        'role': ROLE_ID_FIELD,  # Optional field for role assignment
    },
    required=[],
)

ASSIGNED_REQUEST_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'user_id': openapi.Schema(type=openapi.TYPE_NUMBER, description="User ID"),
        'role_id': ROLE_ID_FIELD,
    },
    required=['user_id', 'role_id'],
)
