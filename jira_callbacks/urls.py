from django.urls import path

from .views.views import ShowJiraInfo

urlpatterns = [
    path("ShowJiraInfo/", ShowJiraInfo.as_view(), name="show_jira_info"),
]
