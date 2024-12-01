from drf_yasg import openapi # type: ignore

# Define reusable Swagger field schemas for permissions
PERMISSION_NAME_FIELD = openapi.Schema(type=openapi.TYPE_STRING, description="Permission name (e.g. 'view_user', 'edit_post')")
DESCRIPTION_FIELD = openapi.Schema(type=openapi.TYPE_STRING, description="Description of the permission")

# Define reusable request bodies for creating and updating permissions
PERMISSION_REQUEST_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'role': openapi.Schema(type=openapi.TYPE_INTEGER, description="Role ID to which the permission is associated"),
        'permission_name': PERMISSION_NAME_FIELD,
        'description': DESCRIPTION_FIELD,
    },
    required=['role', 'permission_name'],
)

# Define response body schema for permission details
PERMISSION_RESPONSE_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Permission ID"),
        'role': openapi.Schema(type=openapi.TYPE_INTEGER, description="Role ID to which the permission is associated"),
        'permission_name': PERMISSION_NAME_FIELD,
        'description': DESCRIPTION_FIELD,
    },
)
