from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Ensure a deterministic local user exists for browser smoke flows."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            default="demo-user",
            help="Username to create or update (default: demo-user).",
        )
        parser.add_argument(
            "--password",
            default="safe-password-123",
            help="Password to set for the smoke user (default: safe-password-123).",
        )

    def handle(self, *args, **options):
        username = options["username"]
        password = options["password"]
        user_model = get_user_model()

        user, created = user_model.objects.get_or_create(username=username)
        user.set_password(password)
        user.save(update_fields=["password"])

        action = "created" if created else "updated"
        self.stdout.write(self.style.SUCCESS(f"Smoke user {action}: username={username}"))
