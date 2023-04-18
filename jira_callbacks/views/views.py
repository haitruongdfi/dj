import rest_framework.status as http_status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


# Create your views here.
class ShowJiraInfo(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return JsonResponse({"message": "Hahaha"})

    def post(self, request, format=None):
        print("===============")
        print(request.data)
        print("===============")
        return Response(
            {"message": "OK"},
            status=http_status.HTTP_200_OK,
        )
