from django.db import models # type: ignore
from model.role.roleModels import RoleModel

class PermissionModel(models.Model):
    # The permission model will be associated with roles
    role = models.ForeignKey(RoleModel, related_name='permissions', on_delete=models.CASCADE)
    permission_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.permission_name} for {self.role.name}'