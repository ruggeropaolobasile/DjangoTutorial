import datetime
from io import StringIO

from django.core.management import call_command
from django.db.models import Sum
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_hero_actions_are_rendered(self):
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "Create Poll")
        self.assertContains(response, "Open Insights")
        self.assertContains(response, "View Showcase")
        self.assertContains(response, "Surprise Me")
        self.assertContains(response, "Download Repo")
        self.assertContains(response, "Open GitHub")
        self.assertContains(response, "Copy Site Markdown")
        self.assertContains(response, "https://github.com/ruggeropaolobasile/DjangoTutorial")

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )

    def test_search_filters_questions(self):
        matching = create_question(question_text="Release planning poll", days=-1)
        create_question(question_text="Team lunch", days=-1)

        response = self.client.get(reverse("polls:index"), {"q": "planning"})

        self.assertQuerySetEqual(response.context["latest_question_list"], [matching])

    def test_popular_sort_orders_by_votes(self):
        popular = create_question(question_text="Popular poll", days=-1)
        less_popular = create_question(question_text="Less popular poll", days=-1)
        Choice.objects.create(question=popular, choice_text="A", votes=8)
        Choice.objects.create(question=less_popular, choice_text="B", votes=1)

        response = self.client.get(reverse("polls:index"), {"sort": "popular"})

        self.assertQuerySetEqual(response.context["latest_question_list"], [popular, less_popular])

    def test_status_filter_returns_ready_polls(self):
        ready = create_question(question_text="Ready poll", days=-1)
        active = create_question(question_text="Active poll", days=-1)
        Choice.objects.create(question=ready, choice_text="A", votes=6)
        Choice.objects.create(question=active, choice_text="B", votes=2)

        response = self.client.get(reverse("polls:index"), {"status": "ready"})

        self.assertQuerySetEqual(response.context["latest_question_list"], [ready])

    def test_dashboard_shows_poll_status_summary(self):
        question = create_question(question_text="Delivery retro", days=-1)
        Choice.objects.create(question=question, choice_text="Keep", votes=4)

        response = self.client.get(reverse("polls:index"))

        self.assertContains(response, "Most Voted Poll")
        self.assertContains(response, "Needs Attention")
        self.assertContains(response, "Healthy")
        self.assertContains(response, "4 vote")
        self.assertContains(response, "Featured Decision")
        self.assertContains(response, "Execution Snapshot")

    def test_dashboard_shows_filter_chips(self):
        create_question(question_text="Delivery retro", days=-1)

        response = self.client.get(
            reverse("polls:index"),
            {"q": "retro", "sort": "popular", "status": "active"},
        )

        self.assertContains(response, "Search: retro")
        self.assertContains(response, "Sort: Popular")
        self.assertContains(response, "Status: Active")


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        create_question(question_text="Second Question.", days=-2)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        self.assertContains(response, "Related Polls")
        self.assertContains(response, "Copy Poll Link")


class PollCreateViewTests(TestCase):
    def test_get_create_page(self):
        response = self.client.get(reverse("polls:create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create a New Poll")
        self.assertContains(response, "distinct choice lines detected")
        self.assertContains(response, "Quick Start Templates")

    def test_template_prefills_create_form(self):
        response = self.client.get(reverse("polls:create"), {"template": "roadmap"})

        self.assertContains(response, "Which feature should we prioritize next sprint?")
        self.assertContains(response, "Automation hub")

    def test_post_creates_poll_and_choices(self):
        response = self.client.post(
            reverse("polls:create"),
            data={
                "question_text": "What should we build next?",
                "choices": "Dashboard\nAPI\nCLI",
            },
        )

        self.assertEqual(Question.objects.count(), 1)
        question = Question.objects.get()
        self.assertEqual(question.question_text, "What should we build next?")
        self.assertEqual(question.choice_set.count(), 3)
        self.assertRedirects(response, reverse("polls:detail", args=(question.id,)))

    def test_post_requires_at_least_two_distinct_choices(self):
        response = self.client.post(
            reverse("polls:create"),
            data={
                "question_text": "Single choice question",
                "choices": "Only one",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please provide at least two distinct choices.")
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(Choice.objects.count(), 0)


class SurprisePollViewTests(TestCase):
    def test_redirects_to_index_when_no_polls(self):
        response = self.client.get(reverse("polls:surprise"))
        self.assertRedirects(response, f"{reverse('polls:index')}?empty=1")

    def test_redirects_to_published_poll(self):
        question = create_question(question_text="Random target", days=-1)
        response = self.client.get(reverse("polls:surprise"))
        self.assertRedirects(response, reverse("polls:detail", args=(question.id,)))


class MvpViewTests(TestCase):
    def test_mvp_page_renders(self):
        response = self.client.get(reverse("polls:mvp"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Decision Loop for Polling Teams")

    def test_mvp_page_shows_poll_data(self):
        poll = create_question(question_text="Roadmap decision", days=-1)
        Choice.objects.create(question=poll, choice_text="Ship", votes=5)

        response = self.client.get(reverse("polls:mvp"))

        self.assertContains(response, "Roadmap decision")
        self.assertContains(response, "5 vote")


class ResultsViewTests(TestCase):
    def test_results_show_lead_margin_and_runner_up(self):
        poll = create_question(question_text="Quarterly focus", days=-1)
        Choice.objects.create(question=poll, choice_text="Automation", votes=7)
        Choice.objects.create(question=poll, choice_text="Reporting", votes=4)

        response = self.client.get(reverse("polls:results", args=(poll.id,)))

        self.assertContains(response, "Lead Margin")
        self.assertContains(response, "3 votes ahead")
        self.assertContains(response, "Reporting")
        self.assertContains(response, "Continue Exploring")
        self.assertContains(response, "Copy Results Link")
        self.assertContains(response, "Create Follow-up Poll")
        self.assertContains(response, "Export Results")

    def test_results_export_returns_plain_text(self):
        poll = create_question(question_text="Quarterly focus", days=-1)
        Choice.objects.create(question=poll, choice_text="Automation", votes=7)

        response = self.client.get(reverse("polls:results_export", args=(poll.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain; charset=utf-8")
        self.assertContains(response, "Poll Results: Quarterly focus")


class InsightsViewTests(TestCase):
    def test_insights_page_renders(self):
        response = self.client.get(reverse("polls:insights"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Polling Performance Snapshot")
        self.assertContains(response, "Leaderboard")

    def test_insights_page_shows_leaderboard_and_quiet_polls(self):
        loud = create_question(question_text="Platform refresh", days=-1)
        quiet = create_question(question_text="Workshop slot", days=-1)
        Choice.objects.create(question=loud, choice_text="Go", votes=6)
        Choice.objects.create(question=quiet, choice_text="Later", votes=1)

        response = self.client.get(reverse("polls:insights"))

        self.assertContains(response, "Platform refresh")
        self.assertContains(response, "Workshop slot")
        self.assertContains(response, "Low traction")
        self.assertContains(response, "Recommended Actions")


class ShowcaseViewTests(TestCase):
    def test_showcase_page_renders(self):
        response = self.client.get(reverse("polls:showcase"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Polls as a decision workspace")
        self.assertContains(response, "Launch a ready-made scenario")


class BriefingViewTests(TestCase):
    def test_briefing_page_renders(self):
        poll = create_question(question_text="Ops review", days=-1)
        Choice.objects.create(question=poll, choice_text="A", votes=5)

        response = self.client.get(reverse("polls:briefing"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Executive Decision Brief")
        self.assertContains(response, "Ops review")
        self.assertContains(response, "Export Briefing")

    def test_briefing_export_returns_plain_text(self):
        poll = create_question(question_text="Ops review", days=-1)
        Choice.objects.create(question=poll, choice_text="A", votes=5)

        response = self.client.get(reverse("polls:briefing_export"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain; charset=utf-8")
        self.assertContains(response, "Polling Studio Briefing")
        self.assertContains(response, "Ops review")


class ReseedDemoDataCommandTests(TestCase):
    def test_reseed_command_creates_mvp_profile_by_default(self):
        out = StringIO()
        call_command("reseed_demo_data", stdout=out)

        self.assertIn("Profile=mvp", out.getvalue())
        self.assertEqual(Question.objects.count(), 8)
        self.assertGreater(Choice.objects.count(), 8)

    def test_reseed_command_replaces_existing_seeded_questions(self):
        call_command("reseed_demo_data", "--profile", "mvp")
        Question.objects.create(
            question_text="Which feature should we ship next quarter?",
            pub_date=timezone.now(),
        )
        self.assertEqual(Question.objects.count(), 9)

        call_command("reseed_demo_data", "--profile", "mvp")

        self.assertEqual(Question.objects.count(), 8)
        self.assertEqual(
            Question.objects.filter(
                question_text="Which feature should we ship next quarter?"
            ).count(),
            1,
        )

    def test_reseed_core_profile_creates_minimal_dataset(self):
        call_command("reseed_demo_data", "--profile", "core")
        self.assertEqual(Question.objects.count(), 5)

    def test_reseed_mvp_profile_covers_search_and_pending_features(self):
        call_command("reseed_demo_data", "--profile", "mvp")

        self.assertTrue(Question.objects.filter(question_text__icontains="planning").exists())
        low_vote_questions = [
            question
            for question in Question.objects.all()
            if (question.choice_set.aggregate(total=Sum("votes"))["total"] or 0) < 3
        ]
        self.assertGreaterEqual(len(low_vote_questions), 1)


class SeedDemoPollsAliasCommandTests(TestCase):
    def test_seed_alias_forwards_to_reseed(self):
        out = StringIO()
        call_command("seed_demo_polls", stdout=out)

        self.assertIn("deprecated; forwarding to reseed_demo_data", out.getvalue())
        self.assertEqual(Question.objects.count(), 8)

    def test_seed_alias_limit_maps_to_profile(self):
        call_command("seed_demo_polls", "--limit", "3")
        self.assertEqual(Question.objects.count(), 5)
