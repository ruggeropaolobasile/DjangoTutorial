import csv
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.views.generic.base import RedirectView, TemplateView

from .forms import PollCreateForm
from .models import AgentSession, Choice, Question

STARTER_TEMPLATES = {
    "roadmap": {
        "label": "Roadmap",
        "question_text": "Which feature should we prioritize next sprint?",
        "choices": "Automation hub\nReporting refresh\nMobile workflow\nAdmin cleanup",
        "description": "Use this when the team needs a fast prioritization decision.",
    },
    "retro": {
        "label": "Retro",
        "question_text": "What should we improve first in the next cycle?",
        "choices": "Planning cadence\nQA handoff\nRelease notes\nSupport loop",
        "description": "Good for internal process improvement and retrospective follow-up.",
    },
    "customer": {
        "label": "Customer",
        "question_text": "Which customer request deserves immediate attention?",
        "choices": "Self-service onboarding\nRole permissions\nExport reliability\nFaster search",
        "description": "Designed for product teams balancing incoming demand.",
    },
}


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    STATUS_LABELS = {
        "all": "All statuses",
        "ready": "Ready",
        "active": "Active",
        "cold": "Cold",
    }

    def get_queryset(self):
        """
        Return published questions with optional search and sorting.
        """
        queryset = Question.objects.filter(pub_date__lte=timezone.now()).annotate(
            total_votes=Sum("choice__votes")
        )
        search_term = self.request.GET.get("q", "").strip()
        sort_key = self.request.GET.get("sort", "recent")
        status_key = self.request.GET.get("status", "all")

        if search_term:
            queryset = queryset.filter(question_text__icontains=search_term)

        if status_key == "ready":
            queryset = queryset.filter(total_votes__gte=5)
        elif status_key == "active":
            queryset = queryset.filter(total_votes__gte=1, total_votes__lt=5)
        elif status_key == "cold":
            queryset = queryset.exclude(total_votes__gte=1)

        if sort_key == "popular":
            queryset = queryset.order_by("-total_votes", "-pub_date")
        else:
            queryset = queryset.order_by("-pub_date")

        return queryset[:8]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repo_url = "https://github.com/ruggeropaolobasile/DjangoTutorial"
        search_term = self.request.GET.get("q", "").strip()
        status_key = self.request.GET.get("status", "all")
        published_questions = Question.objects.filter(pub_date__lte=timezone.now())
        filtered_questions = published_questions.annotate(total_votes=Sum("choice__votes"))
        if search_term:
            filtered_questions = filtered_questions.filter(question_text__icontains=search_term)

        most_voted_poll = (
            published_questions.annotate(total_votes=Sum("choice__votes"))
            .order_by("-total_votes", "-pub_date")
            .first()
        )
        latest_question_list = list(context["latest_question_list"])

        for question in latest_question_list:
            question.total_votes = (
                question.choice_set.aggregate(total_votes=Sum("votes"))["total_votes"] or 0
            )

        context["repo_url"] = repo_url
        context["repo_download_url"] = f"{repo_url}/archive/refs/heads/main.zip"
        context["search_term"] = search_term
        context["sort_key"] = self.request.GET.get("sort", "recent")
        context["status_key"] = status_key
        context["total_polls"] = published_questions.count()
        context["total_votes"] = (
            Choice.objects.filter(question__pub_date__lte=timezone.now()).aggregate(
                total_votes=Sum("votes")
            )["total_votes"]
            or 0
        )
        context["newest_poll"] = published_questions.order_by("-pub_date").first()
        context["most_voted_poll"] = most_voted_poll
        context["active_poll_count"] = sum(
            1 for question in latest_question_list if question.total_votes > 0
        )
        context["stalled_poll_count"] = sum(
            1 for question in latest_question_list if question.total_votes < 3
        )
        context["featured_poll"] = most_voted_poll or context["newest_poll"]
        context["status_counts"] = {
            "ready": filtered_questions.filter(total_votes__gte=5).count(),
            "active": filtered_questions.filter(total_votes__gte=1, total_votes__lt=5).count(),
            "cold": filtered_questions.exclude(total_votes__gte=1).count(),
        }
        context["decision_health"] = [
            {
                "label": "Ready for action",
                "value": sum(1 for question in latest_question_list if question.total_votes >= 5),
            },
            {
                "label": "Collecting signal",
                "value": sum(
                    1 for question in latest_question_list if 1 <= question.total_votes < 5
                ),
            },
            {
                "label": "Still cold",
                "value": sum(1 for question in latest_question_list if question.total_votes == 0),
            },
        ]
        context["starter_templates"] = [
            {"slug": slug, **template_data} for slug, template_data in STARTER_TEMPLATES.items()
        ]
        context["filter_chips"] = [
            chip
            for chip in [
                (
                    {"label": f"Search: {context['search_term']}"}
                    if context["search_term"]
                    else None
                ),
                (
                    {"label": f"Sort: {context['sort_key'].title()}"}
                    if context["sort_key"] != "recent"
                    else None
                ),
                (
                    {"label": f"Status: {context['status_key'].title()}"}
                    if context["status_key"] != "all"
                    else None
                ),
            ]
            if chip
        ]
        has_custom_sort = context["sort_key"] != "recent"
        has_status_filter = status_key != "all"
        has_active_filters = bool(context["search_term"] or has_custom_sort or has_status_filter)
        empty_state_title = "No polls are available."
        empty_state_helper = "Create your first one to get started."

        if has_active_filters:
            if context["search_term"] and not has_status_filter:
                empty_state_title = f"No polls match {context['search_term']}."
            elif has_status_filter and not context["search_term"]:
                empty_state_title = f"No polls are currently in the {status_key} status."
            else:
                parts = []
                if context["search_term"]:
                    parts.append(f"matching '{context['search_term']}'")
                if has_status_filter:
                    parts.append(f"with status '{status_key}'")
                empty_state_title = f"No polls found {' '.join(parts)}."

            empty_state_helper = "Try a different search or remove filters."

        context["has_active_filters"] = has_active_filters
        context["empty_state_title"] = empty_state_title
        context["empty_state_helper"] = empty_state_helper
        context["visible_count"] = len(latest_question_list)
        context["poll_markdown_items"] = [
            {"question_text": question.question_text} for question in latest_question_list
        ]
        context["latest_question_list"] = latest_question_list
        return context


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_polls"] = list(
            Question.objects.filter(pub_date__lte=timezone.now())
            .exclude(pk=self.object.pk)
            .order_by("-pub_date")[:3]
        )
        return context


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        choices = list(context["question"].choice_set.all())
        total_votes = sum(choice.votes for choice in choices)
        sorted_choices = sorted(choices, key=lambda choice: choice.votes, reverse=True)
        context["choices"] = choices
        context["total_votes"] = total_votes
        context["leading_choice"] = (
            max(choices, key=lambda choice: choice.votes) if choices else None
        )
        context["runner_up"] = sorted_choices[1] if len(sorted_choices) > 1 else None
        context["decision_gap"] = (
            sorted_choices[0].votes - sorted_choices[1].votes
            if len(sorted_choices) > 1
            else total_votes
        )
        context["related_polls"] = list(
            Question.objects.filter(pub_date__lte=timezone.now())
            .exclude(pk=self.object.pk)
            .order_by("-pub_date")[:3]
        )
        return context


class CreatePollView(LoginRequiredMixin, generic.FormView):
    template_name = "polls/create.html"
    form_class = PollCreateForm

    def get_initial(self):
        initial = super().get_initial()
        template_key = self.request.GET.get("template", "").strip().lower()
        template_data = STARTER_TEMPLATES.get(template_key)
        if template_data:
            initial["question_text"] = template_data["question_text"]
            initial["choices"] = template_data["choices"]
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["starter_templates"] = [
            {"slug": slug, **template_data} for slug, template_data in STARTER_TEMPLATES.items()
        ]
        selected_template = self.request.GET.get("template", "").strip().lower()
        context["selected_template"] = selected_template
        context["selected_template_detail"] = STARTER_TEMPLATES.get(selected_template)
        return context

    def form_valid(self, form):
        with transaction.atomic():
            question = Question.objects.create(
                question_text=form.cleaned_data["question_text"],
                pub_date=timezone.now(),
                owner=self.request.user,
            )
            Choice.objects.bulk_create(
                [
                    Choice(question=question, choice_text=choice_text)
                    for choice_text in form.cleaned_data["choices"]
                ]
            )
        messages.success(self.request, "Poll created successfully!")
        return HttpResponseRedirect(reverse("polls:detail", args=(question.id,)))


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "polls/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        owned_polls = list(
            Question.objects.filter(owner=self.request.user, pub_date__lte=now)
            .annotate(total_votes=Sum("choice__votes"))
            .order_by("-pub_date")
        )

        for poll in owned_polls:
            poll.total_votes = poll.total_votes or 0

        context["owned_polls"] = owned_polls
        context["owned_poll_count"] = len(owned_polls)
        context["owned_vote_count"] = sum(poll.total_votes for poll in owned_polls)
        return context


class SurprisePollView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        question = Question.objects.filter(pub_date__lte=timezone.now()).order_by("?").first()
        if question:
            return reverse("polls:detail", args=(question.id,))

        query_string = urlencode({"empty": "1"})
        return f"{reverse('polls:index')}?{query_string}"


class MvpView(TemplateView):
    template_name = "polls/mvp.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        polls = list(
            Question.objects.filter(pub_date__lte=timezone.now())
            .annotate(total_votes=Sum("choice__votes"))
            .order_by("-pub_date")[:8]
        )

        total_polls = len(polls)
        total_votes = sum((poll.total_votes or 0) for poll in polls)
        max_votes = max((poll.total_votes or 0) for poll in polls) if polls else 1
        polls_with_votes = sum(1 for poll in polls if (poll.total_votes or 0) > 0)
        activation_rate = round((polls_with_votes / total_polls) * 100) if total_polls else 0

        for poll in polls:
            poll.total_votes = poll.total_votes or 0
            poll.vote_percent = round((poll.total_votes / max_votes) * 100) if max_votes else 0

        context["mvp_metrics"] = {
            "total_polls": total_polls,
            "total_votes": total_votes,
            "activation_rate": activation_rate,
            "pending_actions": sum(1 for poll in polls if poll.total_votes < 3),
        }
        context["mvp_stages"] = [
            {"name": "Collect", "value": total_polls},
            {"name": "Decide", "value": sum(1 for poll in polls if poll.total_votes >= 3)},
            {"name": "Assign", "value": sum(1 for poll in polls if poll.total_votes >= 5)},
            {"name": "Close", "value": sum(1 for poll in polls if poll.total_votes >= 8)},
        ]
        context["mvp_polls"] = polls
        return context


class PricingView(TemplateView):
    template_name = "polls/pricing.html"


class ShowcaseView(TemplateView):
    template_name = "polls/showcase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["showcase_sections"] = [
            {
                "title": "Product planning",
                "body": (
                    "Collect stakeholder signal on roadmap bets, then move the strongest "
                    "option into action."
                ),
            },
            {
                "title": "Team operations",
                "body": "Use concise polls to decide process changes without long async threads.",
            },
            {
                "title": "Customer-facing triage",
                "body": "Turn competing requests into ranked demand with visible rationale.",
            },
        ]
        context["starter_templates"] = [
            {"slug": slug, **template_data} for slug, template_data in STARTER_TEMPLATES.items()
        ]
        return context


class AutomationView(TemplateView):
    template_name = "polls/automation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        smoke_question_text = "Smoke flow: can we create and vote on a poll?"
        user_model = get_user_model()
        published_polls = Question.objects.filter(pub_date__lte=timezone.now())
        smoke_user_exists = user_model.objects.filter(username="demo-user").exists()
        smoke_poll = (
            Question.objects.filter(question_text=smoke_question_text)
            .order_by("-pub_date")
            .first()
        )

        context["automation_metrics"] = {
            "published_poll_count": published_polls.count(),
            "smoke_user_ready": smoke_user_exists,
            "smoke_poll_ready": bool(smoke_poll),
            "insights_ready": published_polls.exists(),
        }
        context["automation_lanes"] = [
            {
                "title": "Autonomous runner",
                "body": (
                    "Uses codex exec item-by-item from the GitHub Project and only keeps going "
                    "when preflight stays green."
                ),
            },
            {
                "title": "Browser smoke",
                "body": (
                    "Prepares a deterministic login/create/vote/results flow so Playwright can "
                    "validate the product slice quickly."
                ),
            },
            {
                "title": "Operator review",
                "body": (
                    "Lets you verify backlog, latest commits and local checks before relaunching "
                    "automation."
                ),
            },
        ]
        context["automation_commands"] = [
            r".\scripts\session-context.ps1",
            r".\scripts\preflight.ps1",
            r".\scripts\playwright-smoke-setup.ps1",
            r".\scripts\autonomous-session.ps1 -CommitOnDone",
        ]
        context["automation_checklist"] = [
            "Working tree clean before starting the runner",
            "Backlog has enough Todo items with Priority and Size",
            "Preflight is green on the active branch",
            "Smoke user and smoke poll are ready for browser checks",
        ]
        context["smoke_poll"] = smoke_poll
        context["recent_sessions"] = AgentSession.objects.order_by("-started_at")[:10]
        return context


class BriefingView(TemplateView):
    template_name = "polls/briefing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        polls = list(
            Question.objects.filter(pub_date__lte=timezone.now())
            .annotate(total_votes=Sum("choice__votes"))
            .order_by("-total_votes", "-pub_date")[:6]
        )

        for poll in polls:
            poll.total_votes = poll.total_votes or 0

        context["briefing_metrics"] = {
            "decision_ready": sum(1 for poll in polls if poll.total_votes >= 5),
            "attention_needed": sum(1 for poll in polls if poll.total_votes < 2),
            "reviewed_polls": len(polls),
        }
        context["briefing_polls"] = polls
        context["briefing_summary"] = [
            "Use this page as an executive walkthrough of current poll signal.",
            "Lead with ready decisions, then show low-traction items needing reach.",
            "Create follow-up polls when a result needs another narrowing step.",
        ]
        return context


class BriefingExportView(TemplateView):
    def get(self, request, *args, **kwargs):
        polls = list(
            Question.objects.filter(pub_date__lte=timezone.now())
            .annotate(total_votes=Sum("choice__votes"))
            .order_by("-total_votes", "-pub_date")[:6]
        )

        lines = [
            "# Polling Studio Briefing",
            "",
            "## Summary",
            "- Executive snapshot of high-signal polls",
            "- Focus on ready decisions and low-traction items",
            "",
            "## Polls",
        ]

        if not polls:
            lines.append("- No published polls available.")
        else:
            for poll in polls:
                vote_total = poll.total_votes or 0
                status = "Ready" if vote_total >= 5 else "Watch"
                lines.append(f"- {poll.question_text} | votes: {vote_total} | status: {status}")

        return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


class ResultsExportView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        question = get_object_or_404(Question, pk=pk, pub_date__lte=timezone.now())
        choices = list(question.choice_set.all())
        total_votes = sum(choice.votes for choice in choices)

        lines = [
            f"# Poll Results: {question.question_text}",
            "",
            f"- Total votes: {total_votes}",
            "",
            "## Options",
        ]

        if not choices:
            lines.append("- No choices configured.")
        else:
            for choice in choices:
                percentage = round((choice.votes / total_votes) * 100) if total_votes else 0
                lines.append(f"- {choice.choice_text}: {choice.votes} vote(s), {percentage}%")

        return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


class InsightsView(TemplateView):
    template_name = "polls/insights.html"

    @staticmethod
    def build_insights_context(filter_key="all"):
        polls = list(
            Question.objects.filter(pub_date__lte=timezone.now())
            .annotate(total_votes=Sum("choice__votes"))
            .order_by("-pub_date")
        )

        for poll in polls:
            poll.total_votes = poll.total_votes or 0

        # Filter logic
        filtered_polls = polls
        if filter_key == "ready":
            filtered_polls = [p for p in polls if p.total_votes >= 5]
        elif filter_key == "active":
            filtered_polls = [p for p in polls if 1 <= p.total_votes < 5]
        elif filter_key == "cold":
            filtered_polls = [p for p in polls if p.total_votes < 1]

        leaderboard = sorted(
            polls,
            key=lambda poll: (poll.total_votes, poll.pub_date),
            reverse=True,
        )[:5]
        quiet_polls = [poll for poll in polls if poll.total_votes < 2][:5]
        total_votes = sum(poll.total_votes for poll in polls)
        engagement_rate = (
            round((sum(1 for poll in polls if poll.total_votes > 0) / len(polls)) * 100)
            if polls
            else 0
        )

        return {
            "insights_metrics": {
                "poll_count": len(polls),
                "vote_count": total_votes,
                "engagement_rate": engagement_rate,
                "quiet_count": len([poll for poll in polls if poll.total_votes < 2]),
            },
            "insight_recommendations": [
                "Promote quiet polls in standup if they sit below 2 votes.",
                "Convert polls above 5 votes into assigned follow-up actions.",
                "Reuse the top-performing question format for the next planning cycle.",
            ],
            "leaderboard": leaderboard,
            "quiet_polls": quiet_polls,
            "recent_polls": filtered_polls[:10],  # Show filtered list
            "filter_key": filter_key,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_key = self.request.GET.get("filter", "all")
        context.update(self.build_insights_context(filter_key))
        return context


class InsightsExportView(TemplateView):
    # ... esistente ...
    def get(self, request, *args, **kwargs):
        context = InsightsView.build_insights_context()
        metrics = context["insights_metrics"]

        lines = [
            "# Polling Performance Snapshot",
            "",
            "## Metrics",
            f"- Published polls: {metrics['poll_count']}",
            f"- Total votes: {metrics['vote_count']}",
            f"- Engagement rate: {metrics['engagement_rate']}%",
            f"- Quiet polls: {metrics['quiet_count']}",
            "",
            "## Leaderboard",
        ]

        if not context["leaderboard"]:
            lines.append("- No published polls yet.")
        else:
            for poll in context["leaderboard"]:
                lines.append(f"- {poll.question_text} | votes: {poll.total_votes}")

        lines.extend(["", "## Needs Attention"])
        if not context["quiet_polls"]:
            lines.append("- All current polls have baseline activity.")
        else:
            for poll in context["quiet_polls"]:
                lines.append(
                    f"- {poll.question_text} | votes: {poll.total_votes} | status: Low traction"
                )

        lines.extend(["", "## Recommended Actions"])
        for recommendation in context["insight_recommendations"]:
            lines.append(f"- {recommendation}")

        # Use text/plain for export
        response = HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="insights-summary.txt"'
        return response


class InsightsCsvExportView(generic.View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="polling-insights.csv"'

        writer = csv.writer(response)
        writer.writerow(["Question Text", "Pub Date", "Total Votes", "Status"])

        polls = Question.objects.filter(pub_date__lte=timezone.now()).annotate(
            total_votes=Sum("choice__votes")
        )

        for poll in polls:
            vote_count = poll.total_votes or 0
            status = "Ready" if vote_count >= 5 else "Active" if vote_count >= 1 else "Cold"
            writer.writerow([
                poll.question_text,
                poll.pub_date.strftime("%Y-%m-%d %H:%M"),
                vote_count,
                status
            ])

        return response


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id, pub_date__lte=timezone.now())
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )

    selected_choice.votes += 1
    selected_choice.save()
    messages.success(request, f"Your vote for '{selected_choice.choice_text}' has been recorded.")
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
