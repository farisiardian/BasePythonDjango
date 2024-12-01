from django.db import models #type: ignore

class PermissionHelperModel(models.Model):
    key = models.CharField(max_length=100, unique=True)  # Unique key for the permission
    name = models.CharField(max_length=200)  # Display name for the permission
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return self.name
