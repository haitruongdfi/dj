import os

from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class GithubSecretApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return JsonResponse({"secret": os.environ["DJ_SECRET_KEY"]})
