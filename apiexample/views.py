from authlib.integrations.django_oauth2 import ResourceProtector
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from . import validator

require_auth = ResourceProtector()
validator = validator.Auth0JWTBearerTokenValidator(
    "dev-m6rvwg1xppktkdnd.us.auth0.com",  # link from Auth0.com identity provider
    "http://localhost:8000",
)
require_auth.register_token_validator(validator)  # this is an decorator for using late


def public(request):
    """No access token required to access this route"""
    response = (
        "Hello from a public endpoint! You don't need to be authenticated to see this."
    )
    return JsonResponse(dict(message=response))


# A private endpoint that requires a valid Access Token JWT.
@require_auth(None)
def private(request):
    """A valid access token is required to access this route"""
    response = "Hello from a private endpoint! You are authenticated to see this."
    return JsonResponse(dict(message=response))


# A private endpoint that requires a valid Access Token JWT containing the given scope (permission).
@require_auth("read:messages")
def private_scoped(request):
    """A valid access token and an appropriate scope are required to access this route"""
    response = "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this."
    return JsonResponse(dict(message=response))


"""
This example uses function-based API View.
References: 
    https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html
    http://itechseeker.com/tutorials/full-stack-development/django/tao-jwt-va-xac-thuc-quyen-truy-cap-trong-django-rest-framework/

After setting and importing decorators, permissions ( on top file ), using 2 decorators to authenticate user
"""


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def sampleJwtAuthProtected(req):
    response = "If you can see this endpoint protected by SimpleJWT, that means you requested API successfully."
    return JsonResponse(dict(message=response))
