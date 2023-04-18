"""djapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from animal import views
from article.views import ArticleView, CommentView


# this snippet to check Sentry.io
def trigger_error1(request):
    division_by_zero = 1 / 0


def trigger_error2(request):
    if a == b:
        print("Unreasonable!")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("articles/", ArticleView.as_view(), name="list-articles"),
    path("animals/", views.hello_reader),
    path("comments/", CommentView.as_view(), name="list-comments"),
    path("apiex/", include("apiexample.urls")),
    path(
        "sentry-debug/", trigger_error2
    ),  # use this for trigger an error for testing Sentry
    path("jira/", include("jira_callbacks.urls")),
]
