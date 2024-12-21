from model.models import RoleModel

def run_role_helper_seeder():
    """
    Seeds the Role table with predefined roles.
    Updates existing records if names match.
    Does not delete roles that no longer exist in the predefined list.
    """
    # Define the roles to seed
    roles = [
        {"name": "Administrator"},
        {"name": "Editor"},
        {"name": "Viewer"},
    ]

    for role_data in roles:
        # Check if the role already exists
        existing_role = RoleModel.objects.filter(name=role_data["name"]).first()

        if existing_role:
            print(f"Role '{role_data['name']}' already exists, skipping creation.")
        else:
            # Create the role if it doesn't exist
            RoleModel.objects.create(name=role_data["name"])
            print(f"Added new role: {role_data['name']}")

    print("Role seeding completed!")