from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore

class RoleModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User, related_name="roles", blank=True)

    def __str__(self):
        return self.name
