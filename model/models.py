from django.db import models # type: ignore

# Swagger
from .swagger.authSwagger import REGISTER_REQUEST_BODY, LOGIN_REQUEST_BODY
from .swagger.userSwagger import USER_REQUEST_BODY

# Serializers
from .user.userSerializers import UserSerializer

# Create your models here.
