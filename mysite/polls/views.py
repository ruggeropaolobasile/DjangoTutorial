from urllib.parse import urlencode

from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.views.generic.base import RedirectView, TemplateView

from .forms import PollCreateForm
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return published questions with optional search and sorting.
        """
        queryset = Question.objects.filter(pub_date__lte=timezone.now())
        search_term = self.request.GET.get("q", "").strip()
        sort_key = self.request.GET.get("sort", "recent")

        if search_term:
            queryset = queryset.filter(question_text__icontains=search_term)

        if sort_key == "popular":
            queryset = queryset.annotate(total_votes=Sum("choice__votes")).order_by(
                "-total_votes", "-pub_date"
            )
        else:
            queryset = queryset.order_by("-pub_date")

        return queryset[:8]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repo_url = "https://github.com/ruggeropaolobasile/DjangoTutorial"
        published_questions = Question.objects.filter(pub_date__lte=timezone.now())
        context["repo_url"] = repo_url
        context["repo_download_url"] = f"{repo_url}/archive/refs/heads/main.zip"
        context["search_term"] = self.request.GET.get("q", "").strip()
        context["sort_key"] = self.request.GET.get("sort", "recent")
        context["total_polls"] = published_questions.count()
        context["total_votes"] = (
            Choice.objects.filter(question__pub_date__lte=timezone.now()).aggregate(
                total_votes=Sum("votes")
            )["total_votes"]
            or 0
        )
        context["newest_poll"] = published_questions.order_by("-pub_date").first()
        context["poll_markdown_items"] = [
            {"question_text": question.question_text}
            for question in context["latest_question_list"]
        ]
        return context


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        choices = list(context["question"].choice_set.all())
        total_votes = sum(choice.votes for choice in choices)
        context["choices"] = choices
        context["total_votes"] = total_votes
        return context


class CreatePollView(generic.FormView):
    template_name = "polls/create.html"
    form_class = PollCreateForm

    def form_valid(self, form):
        with transaction.atomic():
            question = Question.objects.create(
                question_text=form.cleaned_data["question_text"],
                pub_date=timezone.now(),
            )
            Choice.objects.bulk_create(
                [
                    Choice(question=question, choice_text=choice_text)
                    for choice_text in form.cleaned_data["choices"]
                ]
            )
        return HttpResponseRedirect(reverse("polls:detail", args=(question.id,)))


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
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
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
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
