from model.models import PermissionHelperModel  # Adjust the import to your model location

def run_permission_helper_seeder():
    """
    Seeds the PermissionHelper table with predefined permissions.
    Updates existing records if keys match.
    """
    permissions = [
        {"key": "create_users", "name": "Create Users", "description": "Allows user creation"},
        {"key": "edit_users", "name": "Edit Users", "description": "Allows user editing"},
        {"key": "delete_users", "name": "Delete Users", "description": "Allows user deletion"},
        {"key": "view_users", "name": "View Users", "description": "Allows viewing users"},
        {"key": "create_role", "name": "Create Role", "description": "Allows role creation"},
        {"key": "edit_role", "name": "Edit Role", "description": "Allows role editing"},
        {"key": "delete_role", "name": "Delete Role", "description": "Allows role deletion"},
        {"key": "view_role", "name": "View Role", "description": "Allows viewing role"},
    ]

    for permission in permissions:
        obj, created = PermissionHelperModel.objects.update_or_create(
            key=permission["key"],
            defaults={"name": permission["name"], "description": permission["description"]},
        )
        if created:
            print(f"Added new permission: {permission['name']}")
        else:
            print(f"Updated existing permission: {permission['name']}")

    print("PermissionHelper seeding completed!")
