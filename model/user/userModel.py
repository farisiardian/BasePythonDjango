from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
from model.models import RoleModel

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.ForeignKey(RoleModel, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")

    def __str__(self):
        return f"{self.user.username}'s Profile"
