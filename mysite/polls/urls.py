from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("briefing/", views.BriefingView.as_view(), name="briefing"),
    path("briefing/export/", views.BriefingExportView.as_view(), name="briefing_export"),
    path("create/", views.CreatePollView.as_view(), name="create"),
    path("insights/", views.InsightsView.as_view(), name="insights"),
    path("mvp/", views.MvpView.as_view(), name="mvp"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("showcase/", views.ShowcaseView.as_view(), name="showcase"),
    path("surprise/", views.SurprisePollView.as_view(), name="surprise"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:pk>/results/export/", views.ResultsExportView.as_view(), name="results_export"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
"""
v1
app_name = "polls"
urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
"""
