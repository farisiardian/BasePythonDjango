from drf_yasg import openapi # type: ignore

# Define field schema for role name
ROLE_NAME_FIELD = openapi.Schema(
    type=openapi.TYPE_STRING,
    description="Role name (e.g., 'Admin', 'User')"
)

# Define request body schema for creating and updating a role
ROLE_REQUEST_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': ROLE_NAME_FIELD,
    },
    required=['name'],
)

# Define response body schema for a single role
ROLE_RESPONSE_BODY_SINGLE = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Role ID"),
        'name': ROLE_NAME_FIELD,
    },
)

# Define response body schema for a list of roles
ROLE_RESPONSE_BODY_LIST = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=ROLE_RESPONSE_BODY_SINGLE,
)
