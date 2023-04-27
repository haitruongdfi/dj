from django.urls import path

from .views.views import ShowJiraInfo, GetTempoTokens, GetTempoWorklog

urlpatterns = [
    path("ShowJiraInfo/", ShowJiraInfo.as_view(), name="show_jira_info"),
    path("GetTempoTokens/", GetTempoTokens.as_view(), name="get_tempo_tokens"),
    path("GetTempoWorklog/", GetTempoWorklog.as_view(), name="get_tempo_worklog"),
]
