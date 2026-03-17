from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("automation/", views.AutomationView.as_view(), name="automation"),
    path("", views.IndexView.as_view(), name="index"),
    path("briefing/", views.BriefingView.as_view(), name="briefing"),
    path("briefing/export/", views.BriefingExportView.as_view(), name="briefing_export"),
    path("create/", views.CreatePollView.as_view(), name="create"),
    path("insights/", views.InsightsView.as_view(), name="insights"),
    path("insights/export/", views.InsightsExportView.as_view(), name="insights_export"),
    path("mvp/", views.MvpView.as_view(), name="mvp"),
    path("pricing/", views.PricingView.as_view(), name="pricing"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("showcase/", views.ShowcaseView.as_view(), name="showcase"),
    path("surprise/", views.SurprisePollView.as_view(), name="surprise"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:pk>/results/export/", views.ResultsExportView.as_view(), name="results_export"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
