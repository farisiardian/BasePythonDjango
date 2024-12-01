from drf_yasg import openapi # type: ignore

# Define reusable Swagger field schemas for roles
ROLE_NAME_FIELD = openapi.Schema(type=openapi.TYPE_STRING, description="Role name (e.g. 'Admin', 'User')")

# Define reusable request bodies for creating and updating roles
ROLE_REQUEST_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': ROLE_NAME_FIELD,
    },
    required=['name'],
)

# Define response body schema for role details
ROLE_RESPONSE_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Role ID"),
        'name': ROLE_NAME_FIELD,
    },
)
