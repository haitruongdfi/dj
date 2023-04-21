import json
import time

import rest_framework.status as http_status
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class ShowJiraInfo(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return JsonResponse({"message": "Hahaha"})

    def post(self, request, format=None):
        print("===============")
        file_name = f"result{round(time.time())}.json"
        with open(file_name, "a") as f:
            f.write(json.dumps(request.data, indent=4))
            # f.write("==========end of each request=========")

        print("===============")
        return Response(
            {"message": "OK"},
            status=http_status.HTTP_200_OK,
        )
