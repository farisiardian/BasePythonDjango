from django.db import models # type: ignore

# Swagger
from .swagger.authSwagger import REGISTER_REQUEST_BODY, LOGIN_REQUEST_BODY
from .swagger.userSwagger import USER_REQUEST_BODY, ASSIGNED_REQUEST_BODY
from .swagger.roleSwagger import ROLE_NAME_FIELD, ROLE_REQUEST_BODY, ROLE_RESPONSE_BODY
from .swagger.permissionSwagger import PERMISSION_NAME_FIELD, DESCRIPTION_FIELD, PERMISSION_REQUEST_BODY, PERMISSION_RESPONSE_BODY

# Models
from .role.roleModels import RoleModel
from .permission.permissionModels import PermissionModel
from .permission.permissionHelperModel import PermissionHelperModel

# Serializers
from .user.userSerializers import (
    UserSerializer,
    UserProfileSerializer
)
from .role.roleSerializers import RoleSerializer
from .permission.permissionSerializers import PermissionSerializer
from .permission.permissionHelperSerializers import PermissionHelperSerializer