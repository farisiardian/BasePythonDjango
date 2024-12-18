from model.models import PermissionModel, RoleModel

def run_permission_helper_seeder():
    """
    Seeds the Permission table by role with predefined permissions.
    Updates existing records if keys match.
    Deletes permissions that no longer exist.
    """
    # Define the permissions to seed for roles
    permissions = [
        {"permission_name": "create_users", "description": "Allows user creation"},
        {"permission_name": "edit_users", "description": "Allows user editing"},
        {"permission_name": "delete_users", "description": "Allows user deletion"},
        {"permission_name": "view_users", "description": "Allows viewing users"},
        {"permission_name": "create_role", "description": "Allows role creation"},
        {"permission_name": "edit_role", "description": "Allows role editing"},
        {"permission_name": "delete_role", "description": "Allows role deletion"},
        {"permission_name": "view_role", "description": "Allows viewing role"},
        {"permission_name": "edit_permission", "description": "Allows permission editing"},
        {"permission_name": "view_permission", "description": "Allows viewing permission"},
    ]

    # Fetch all roles in the system
    roles = RoleModel.objects.all()

    for role in roles:
        print(f"Seeding permissions for role: {role.name}")

        # Get current permissions for the role
        current_permissions = PermissionModel.objects.filter(role=role)

        # Go through the predefined permissions and handle them
        for permission in permissions:
            # Check if permission exists for the current role
            existing_permission = current_permissions.filter(permission_name=permission["permission_name"]).first()

            if existing_permission:
                if(role.id == 1) :
                    # Update the permission if it exists
                    existing_permission.description = permission["description"]
                    existing_permission.is_permission = True  # Set to false initially
                    existing_permission.save()
                    print(f"Updated existing permission: {permission['permission_name']} for role {role.name}")
                else :
                    # Update the permission if it exists
                    existing_permission.description = permission["description"]
                    existing_permission.is_permission = False  # Set to false initially
                    existing_permission.save()
                    print(f"Updated existing permission: {permission['permission_name']} for role {role.name}")
            else:
                if(role.id == 1) :
                    # Create a new permission if it doesn't exist
                    PermissionModel.objects.create(
                        role=role,
                        permission_name=permission["permission_name"],
                        description=permission["description"],
                        is_permission=True  # Initially set to false
                    )
                    print(f"Added new permission: {permission['permission_name']} for role {role.name}")
                else :
                    # Create a new permission if it doesn't exist
                    PermissionModel.objects.create(
                        role=role,
                        permission_name=permission["permission_name"],
                        description=permission["description"],
                        is_permission=False  # Initially set to false
                    )
                    print(f"Added new permission: {permission['permission_name']} for role {role.name}")

        # Handle deleted permissions: remove permissions not in the list anymore
        permission_names = [p["permission_name"] for p in permissions]
        permissions_to_delete = current_permissions.exclude(permission_name__in=permission_names)

        for permission in permissions_to_delete:
            permission.delete()
            print(f"Deleted permission: {permission.permission_name} for role {role.name}")

    print("Permission seeding completed!")
