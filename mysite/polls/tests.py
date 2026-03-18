import datetime
from io import StringIO

from django.contrib.auth import get_user_model
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


class QuestionAdminTests(TestCase):
    def test_changelist_shows_owner_column_and_loads(self):
        admin_user = get_user_model().objects.create_superuser(
            username="admin-user",
            password="password",
        )
        owner = get_user_model().objects.create_user(
            username="owner-user",
            password="password",
        )
        Question.objects.create(
            question_text="Owned question",
            pub_date=timezone.now(),
            owner=owner,
        )

        self.client.force_login(admin_user)
        response = self.client.get(reverse("admin:polls_question_changelist"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "column-owner")
        self.assertContains(response, "owner-user")


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

    def test_search_empty_state_is_contextual_when_no_results_match(self):
        create_question(question_text="Release planning poll", days=-1)

        response = self.client.get(reverse("polls:index"), {"q": "finance"})

        self.assertQuerySetEqual(response.context["latest_question_list"], [])
        self.assertContains(response, "No polls match finance.")
        self.assertContains(response, "Try a different search or remove filters.")

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

    def test_status_empty_state_is_contextual_when_filter_has_no_results(self):
        poll = create_question(question_text="Fresh poll", days=-1)
        Choice.objects.create(question=poll, choice_text="A", votes=1)

        response = self.client.get(reverse("polls:index"), {"status": "ready"})

        self.assertQuerySetEqual(response.context["latest_question_list"], [])
        self.assertContains(response, "No polls are currently in the ready status.")
        self.assertContains(response, "Try a different search or remove filters.")

    def test_header_shows_ready_active_cold_counts(self):
        ready = create_question(question_text="Ready poll", days=-1)
        active = create_question(question_text="Active poll", days=-1)
        cold = create_question(question_text="Cold poll", days=-1)
        future = create_question(question_text="Future poll", days=2)
        Choice.objects.create(question=ready, choice_text="A", votes=5)
        Choice.objects.create(question=active, choice_text="B", votes=3)
        Choice.objects.create(question=future, choice_text="C", votes=9)
        Choice.objects.create(question=cold, choice_text="D", votes=0)

        response = self.client.get(reverse("polls:index"))

        self.assertContains(response, "Ready 1 · Active 1 · Cold 1")

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
        self.assertContains(response, "Created at")
        self.assertContains(response, "Related Polls")
        self.assertContains(response, "Copy Poll Link")


class PollCreateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="demo-user",
            password="safe-password-123",
        )

    def test_get_create_page(self):
        self.client.login(username="demo-user", password="safe-password-123")
        response = self.client.get(reverse("polls:create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create a New Poll")
        self.assertContains(response, "distinct choice lines detected")
        self.assertContains(response, "Quick Start Templates")

    def test_create_requires_authentication(self):
        response = self.client.get(reverse("polls:create"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_template_prefills_create_form(self):
        self.client.login(username="demo-user", password="safe-password-123")
        response = self.client.get(reverse("polls:create"), {"template": "roadmap"})

        self.assertContains(response, "Which feature should we prioritize next sprint?")
        self.assertContains(response, "Automation hub")

    def test_post_creates_poll_and_choices(self):
        self.client.login(username="demo-user", password="safe-password-123")
        response = self.client.post(
            reverse("polls:create"),
            data={
                "question_text": "What should we build next?",
                "choices": "Dashboard\nAPI\nCLI",
            },
            follow=True,
        )

        self.assertEqual(Question.objects.count(), 1)
        question = Question.objects.get()
        self.assertEqual(question.question_text, "What should we build next?")
        self.assertEqual(question.owner, self.user)
        self.assertEqual(question.choice_set.count(), 3)
        self.assertRedirects(response, reverse("polls:detail", args=(question.id,)))
        self.assertContains(response, "Poll created successfully!")

    def test_post_requires_at_least_two_distinct_choices(self):
        self.client.login(username="demo-user", password="safe-password-123")
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

    def test_post_deduplicates_choices(self):
        self.client.login(username="demo-user", password="safe-password-123")
        self.client.post(
            reverse("polls:create"),
            data={
                "question_text": "Duplicate choice test",
                "choices": "A\nA\nB\nB\nC",
            },
        )

        question = Question.objects.get(question_text="Duplicate choice test")
        self.assertEqual(question.choice_set.count(), 3)
        self.assertQuerySetEqual(
            question.choice_set.order_by("choice_text"),
            ["A", "B", "C"],
            transform=lambda c: c.choice_text,
        )


class AuthFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="demo-user",
            password="safe-password-123",
        )

    def test_login_page_renders(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign in")
        self.assertContains(response, "Welcome back")

    def test_base_navigation_shows_sign_in_for_anonymous_users(self):
        response = self.client.get(reverse("polls:index"))

        self.assertContains(response, "Sign in")
        self.assertContains(response, "Automation")
        self.assertNotContains(response, "Sign out")
        self.assertNotContains(response, "Profile")
        self.assertNotContains(response, reverse("polls:profile"))

    def test_login_redirects_to_index_and_updates_navigation(self):
        response = self.client.post(
            reverse("login"),
            data={"username": "demo-user", "password": "safe-password-123"},
            follow=True,
        )

        self.assertRedirects(response, reverse("polls:index"))
        self.assertContains(response, "Profile")
        self.assertContains(response, "Signed in as demo-user")
        self.assertContains(response, "Sign out")
        self.assertContains(response, reverse("polls:profile"))
        self.assertContains(response, "Welcome back, demo-user!")

    def test_logout_redirects_to_index(self):
        self.client.login(username="demo-user", password="safe-password-123")

        response = self.client.post(reverse("logout"), follow=True)

        self.assertRedirects(response, reverse("polls:index"))
        self.assertContains(response, "Sign in")
        self.assertNotContains(response, "Signed in as demo-user")
        self.assertContains(response, "You have successfully signed out.")


class SurprisePollViewTests(TestCase):
    def test_redirects_to_index_when_no_polls(self):
        response = self.client.get(reverse("polls:surprise"))
        self.assertRedirects(response, f"{reverse('polls:index')}?empty=1")

    def test_redirects_to_published_poll(self):
        question = create_question(question_text="Random target", days=-1)
        response = self.client.get(reverse("polls:surprise"))
        self.assertRedirects(response, reverse("polls:detail", args=(question.id,)))


class ProfileViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="demo-user",
            password="safe-password-123",
        )
        self.other_user = get_user_model().objects.create_user(
            username="other-user",
            password="safe-password-123",
        )

    def test_profile_requires_authentication(self):
        response = self.client.get(reverse("polls:profile"))

        expected_redirect = f"{reverse('login')}?next={reverse('polls:profile')}"
        self.assertRedirects(response, expected_redirect)

    def test_profile_shows_empty_state_when_user_has_no_owned_polls(self):
        self.client.login(username="demo-user", password="safe-password-123")

        response = self.client.get(reverse("polls:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No owned polls yet")
        self.assertContains(response, "Create Your First Poll")
        self.assertContains(response, reverse("polls:create"))

    def test_profile_lists_only_owned_polls(self):
        owned = Question.objects.create(
            question_text="Owned roadmap",
            pub_date=timezone.now(),
            owner=self.user,
        )
        other = Question.objects.create(
            question_text="Other roadmap",
            pub_date=timezone.now(),
            owner=self.other_user,
        )
        Choice.objects.create(question=owned, choice_text="Ship", votes=4)
        Choice.objects.create(question=other, choice_text="Wait", votes=2)
        self.client.login(username="demo-user", password="safe-password-123")

        response = self.client.get(reverse("polls:profile"))

        self.assertContains(response, "Owned roadmap")
        self.assertNotContains(response, "Other roadmap")
        self.assertEqual(response.context["owned_polls"][0], owned)

    def test_profile_shows_owned_poll_summary_metrics(self):
        first_poll = Question.objects.create(
            question_text="First owned roadmap",
            pub_date=timezone.now(),
            owner=self.user,
        )
        second_poll = Question.objects.create(
            question_text="Second owned roadmap",
            pub_date=timezone.now(),
            owner=self.user,
        )
        Question.objects.create(
            question_text="Other user roadmap",
            pub_date=timezone.now(),
            owner=self.other_user,
        )
        Choice.objects.create(question=first_poll, choice_text="Ship", votes=4)
        Choice.objects.create(question=first_poll, choice_text="Wait", votes=1)
        Choice.objects.create(question=second_poll, choice_text="Expand", votes=3)
        self.client.login(username="demo-user", password="safe-password-123")

        response = self.client.get(reverse("polls:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["owned_poll_count"], 2)
        self.assertEqual(response.context["owned_vote_count"], 8)
        self.assertContains(response, "Polls Created")
        self.assertContains(response, "Total Votes Received")
        self.assertContains(response, "<strong>2</strong>", html=True)
        self.assertContains(response, "<strong>8</strong>", html=True)


class AutomationViewTests(TestCase):
    def test_automation_page_renders_runtime_snapshot(self):
        response = self.client.get(reverse("polls:automation"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Automation Control Room")
        self.assertContains(response, "Runtime Snapshot")
        self.assertContains(response, r".\scripts\autonomous-session.ps1 -CommitOnDone")
        self.assertContains(response, "Smoke Poll")

    def test_automation_page_links_to_smoke_poll_when_available(self):
        smoke_poll = Question.objects.create(
            question_text="Smoke flow: can we create and vote on a poll?",
            pub_date=timezone.now(),
        )

        response = self.client.get(reverse("polls:automation"))

        self.assertContains(response, smoke_poll.question_text)
        self.assertContains(response, reverse("polls:detail", args=(smoke_poll.id,)))


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

    def test_mvp_page_contains_pricing_link(self):
        response = self.client.get(reverse("polls:mvp"))
        self.assertContains(response, reverse("polls:pricing"))


class PricingViewTests(TestCase):
    def test_pricing_page_renders(self):
        response = self.client.get(reverse("polls:pricing"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Simple plans for decision-driven teams")
        self.assertContains(response, "Starter")
        self.assertContains(response, "Business")

class ResultsViewTests(TestCase):
    def test_results_show_zero_vote_empty_state(self):
        poll = create_question(question_text="Quarterly focus", days=-1)
        Choice.objects.create(question=poll, choice_text="Automation", votes=0)
        Choice.objects.create(question=poll, choice_text="Reporting", votes=0)

        response = self.client.get(reverse("polls:results", args=(poll.id,)))

        self.assertContains(
            response,
            "No votes yet. Share this poll to collect the first response.",
        )

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


class VoteViewTests(TestCase):
    def test_successful_vote_shows_message(self):
        question = create_question(question_text="Voting test poll", days=-1)
        choice = Choice.objects.create(question=question, choice_text="Vote for me")

        response = self.client.post(
            reverse("polls:vote", args=(question.id,)),
            data={"choice": choice.id},
            follow=True,
        )

        self.assertRedirects(response, reverse("polls:results", args=(question.id,)))
        # Note: quotes are escaped in HTML rendering
        self.assertContains(
            response,
            f"Your vote for &#x27;{choice.choice_text}&#x27; has been recorded.",
        )

    def test_future_question_cannot_be_voted_on(self):
        question = create_question(question_text="Future question.", days=5)
        choice = Choice.objects.create(question=question, choice_text="Wait")

        response = self.client.post(
            reverse("polls:vote", args=(question.id,)),
            data={"choice": choice.id},
        )

        choice.refresh_from_db()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(choice.votes, 0)


class BrowserSmokeFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="demo-user",
            password="safe-password-123",
        )

    def test_login_create_vote_results_flow(self):
        login_response = self.client.post(
            reverse("login"),
            data={"username": "demo-user", "password": "safe-password-123"},
        )
        self.assertRedirects(login_response, reverse("polls:index"))

        create_response = self.client.post(
            reverse("polls:create"),
            data={
                "question_text": "Smoke flow question",
                "choices": "Option A\nOption B",
            },
        )
        self.assertEqual(Question.objects.count(), 1)
        question = Question.objects.get()
        self.assertRedirects(create_response, reverse("polls:detail", args=(question.id,)))

        choice = question.choice_set.get(choice_text="Option A")
        vote_response = self.client.post(
            reverse("polls:vote", args=(question.id,)),
            data={"choice": choice.id},
        )
        self.assertRedirects(vote_response, reverse("polls:results", args=(question.id,)))

        results_response = self.client.get(reverse("polls:results", args=(question.id,)))
        self.assertContains(results_response, "Smoke flow question")
        self.assertContains(results_response, "Total votes collected:")
        self.assertContains(results_response, "1 vote")
        self.assertContains(results_response, "Option A")


class InsightsViewTests(TestCase):
    def test_insights_page_renders(self):
        response = self.client.get(reverse("polls:insights"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Polling Performance Snapshot")
        self.assertContains(response, "Leaderboard")
        self.assertContains(response, "Export Summary (TXT)")

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

    def test_insights_export_returns_plain_text_attachment(self):
        loud = create_question(question_text="Platform refresh", days=-1)
        quiet = create_question(question_text="Workshop slot", days=-1)
        Choice.objects.create(question=loud, choice_text="Go", votes=6)
        Choice.objects.create(question=quiet, choice_text="Later", votes=1)

        response = self.client.get(reverse("polls:insights_export"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain; charset=utf-8")
        self.assertEqual(
            response["Content-Disposition"],
            'attachment; filename="insights-summary.txt"',
        )
        self.assertContains(response, "Polling Performance Snapshot")
        self.assertContains(response, "Published polls: 2")
        self.assertContains(response, "Platform refresh | votes: 6")
        self.assertContains(response, "Workshop slot | votes: 1 | status: Low traction")


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


class EnsureSmokeUserCommandTests(TestCase):
    def test_command_creates_default_smoke_user(self):
        out = StringIO()

        call_command("ensure_smoke_user", stdout=out)

        user = get_user_model().objects.get(username="demo-user")
        self.assertTrue(user.check_password("safe-password-123"))
        self.assertIn("Smoke user created: username=demo-user", out.getvalue())

    def test_command_updates_existing_user_password(self):
        user_model = get_user_model()
        user_model.objects.create_user(username="demo-user", password="old-password")

        call_command("ensure_smoke_user", "--password", "new-password")

        user = user_model.objects.get(username="demo-user")
        self.assertTrue(user.check_password("new-password"))


class EnsureSmokePollCommandTests(TestCase):
    def test_command_creates_default_smoke_poll(self):
        out = StringIO()

        call_command("ensure_smoke_poll", stdout=out)

        poll = Question.objects.get(question_text="Smoke flow: can we create and vote on a poll?")
        self.assertEqual(poll.owner.username, "demo-user")
        self.assertLessEqual(poll.pub_date, timezone.now())
        self.assertEqual(
            list(poll.choice_set.order_by("choice_text").values_list("choice_text", flat=True)),
            ["Option A", "Option B"],
        )
        self.assertIn("Smoke poll created", out.getvalue())

    def test_command_resets_existing_smoke_poll_to_deterministic_state(self):
        user_model = get_user_model()
        stale_owner = user_model.objects.create_user(username="stale-owner", password="password")
        poll = Question.objects.create(
            question_text="Smoke flow: can we create and vote on a poll?",
            pub_date=timezone.now() - datetime.timedelta(days=7),
            owner=stale_owner,
        )
        Choice.objects.create(question=poll, choice_text="Option A", votes=9)
        Choice.objects.create(question=poll, choice_text="Legacy option", votes=3)
        Question.objects.create(
            question_text="Smoke flow: can we create and vote on a poll?",
            pub_date=timezone.now() - datetime.timedelta(days=8),
        )

        call_command("ensure_smoke_poll")

        poll.refresh_from_db()
        self.assertEqual(
            Question.objects.filter(
                question_text="Smoke flow: can we create and vote on a poll?"
            ).count(),
            1,
        )
        self.assertEqual(poll.owner.username, "demo-user")
        self.assertEqual(
            list(poll.choice_set.order_by("choice_text").values_list("choice_text", "votes")),
            [("Option A", 0), ("Option B", 0)],
        )
