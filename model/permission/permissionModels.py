from django.db import models
from model.role.roleModels import RoleModel

class PermissionModel(models.Model):
    role = models.ForeignKey(RoleModel, related_name='permissions', on_delete=models.CASCADE)
    permission_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_permission = models.BooleanField(default=False)  # False by default

    def __str__(self):
        return f'{self.permission_name} for {self.role.name}'
