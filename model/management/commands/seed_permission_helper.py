from django.core.management.base import BaseCommand # type: ignore
from model.permission.permissionHelperSeeder import run_permission_helper_seeder

class Command(BaseCommand):
    help = "Seed the PermissionHelper table with predefined permissions"

    def handle(self, *args, **options):
        run_permission_helper_seeder()
        self.stdout.write(self.style.SUCCESS("Permissions seeded successfully!"))