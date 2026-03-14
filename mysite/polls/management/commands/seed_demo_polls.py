from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Backward-compatible alias for reseed_demo_data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Kept for compatibility. Data is always reseeded.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=8,
            help="Compatibility option mapped to profile (core<=5, mvp<=8, full>8).",
        )

    def handle(self, *args, **options):
        limit = max(1, options["limit"])
        if limit <= 5:
            profile = "core"
        elif limit <= 8:
            profile = "mvp"
        else:
            profile = "full"

        self.stdout.write(
            self.style.WARNING(
                "seed_demo_polls is deprecated; forwarding to reseed_demo_data "
                f"(profile={profile})."
            )
        )
        call_command("reseed_demo_data", "--profile", profile)
