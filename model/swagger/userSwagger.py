from drf_yasg import openapi # type: ignore

# Define reusable Swagger field schemas
USERNAME_FIELD = openapi.Schema(type=openapi.TYPE_STRING, description="Username")
EMAIL_FIELD = openapi.Schema(type=openapi.TYPE_STRING, description="Email address")
PASSWORD_FIELD = openapi.Schema(type=openapi.TYPE_STRING, description="Password")

# Define reusable request bodies
USER_REQUEST_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': USERNAME_FIELD,
        'email': EMAIL_FIELD,
        'password': PASSWORD_FIELD,
    },
    required=['username', 'email', 'password'],
)