from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from polls.demo_seed import PROFILE_LIMITS, polls_for_profile, seeded_question_texts
from polls.models import Choice, Question


class Command(BaseCommand):
    help = "Reset and recreate deterministic demo data for development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--profile",
            choices=sorted(PROFILE_LIMITS.keys()),
            default="mvp",
            help="Dataset profile: core, mvp, or full (default: mvp).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print what would happen without changing the database.",
        )

    def handle(self, *args, **options):
        profile = options["profile"]
        demo_polls = polls_for_profile(profile)
        question_texts = set(seeded_question_texts())

        if options["dry_run"]:
            self.stdout.write(
                self.style.WARNING(
                    f"[dry-run] Profile={profile}. Would reseed {len(demo_polls)} poll(s)."
                )
            )
            return

        now = timezone.now()
        with transaction.atomic():
            deleted_rows, _ = Question.objects.filter(question_text__in=question_texts).delete()
            created_questions = 0
            created_choices = 0

            for poll in demo_polls:
                question = Question.objects.create(
                    question_text=poll.question_text,
                    pub_date=now - timedelta(days=poll.age_days, hours=poll.age_hours),
                )
                choices = [
                    Choice(question=question, choice_text=choice_text, votes=votes)
                    for choice_text, votes in poll.choices
                ]
                Choice.objects.bulk_create(choices)
                created_questions += 1
                created_choices += len(choices)

        self.stdout.write(self.style.WARNING(f"Removed {deleted_rows} existing demo row(s)."))
        self.stdout.write(
            self.style.SUCCESS(
                "Reseed complete. "
                f"Profile={profile}, questions={created_questions}, choices={created_choices}."
            )
        )
