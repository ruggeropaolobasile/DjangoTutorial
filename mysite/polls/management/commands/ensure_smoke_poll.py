from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from polls.models import Choice, Question

SMOKE_POLL_QUESTION = "Smoke flow: can we create and vote on a poll?"
SMOKE_POLL_CHOICES = ("Option A", "Option B")


class Command(BaseCommand):
    help = "Ensure a deterministic poll exists for demo and smoke flows."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            default="demo-user",
            help="Owner username to create or update for the smoke poll (default: demo-user).",
        )

    def handle(self, *args, **options):
        username = options["username"]
        user_model = get_user_model()

        with transaction.atomic():
            owner, _ = user_model.objects.get_or_create(username=username)

            existing_questions = list(
                Question.objects.filter(question_text=SMOKE_POLL_QUESTION).order_by("id")
            )
            question = (
                existing_questions[0]
                if existing_questions
                else Question(question_text=SMOKE_POLL_QUESTION)
            )
            duplicate_ids = [item.id for item in existing_questions[1:]]

            question.pub_date = timezone.now() - timedelta(minutes=5)
            question.owner = owner
            question.save()

            if duplicate_ids:
                Question.objects.filter(id__in=duplicate_ids).delete()

            existing_choices = {
                choice.choice_text: choice for choice in Choice.objects.filter(question=question)
            }
            for choice_text in SMOKE_POLL_CHOICES:
                choice = existing_choices.pop(choice_text, None)
                if choice is None:
                    Choice.objects.create(question=question, choice_text=choice_text, votes=0)
                    continue
                if choice.votes != 0:
                    choice.votes = 0
                    choice.save(update_fields=["votes"])

            if existing_choices:
                Choice.objects.filter(
                    id__in=[choice.id for choice in existing_choices.values()]
                ).delete()

        action = "created" if not existing_questions else "updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"Smoke poll {action}: question='{SMOKE_POLL_QUESTION}', owner={username}"
            )
        )
