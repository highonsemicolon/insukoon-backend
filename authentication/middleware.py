import re

from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the requested path is exempt from authentication
        if self.is_exempt_path(request.path):
            return self.get_response(request)

        token = None
        # Check if the user is authenticated via token
        if 'HTTP_AUTHORIZATION' in request.META:
            try:
                token_key = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
                token = Token.objects.get(key=token_key)
                request.user = token.user
            except Token.DoesNotExist:
                pass  # Token is invalid
            except IndexError:
                pass

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        # if not request.user.is_email_verified:
        #     return JsonResponse({'error': 'Email not verified'}, status=403)

        # Check if the requested path is exempt from payment check
        if not self.is_exempt_path(request.path, payment_exempt=True):
            # Check if the user is a paid user
            request.user = token.user
            if not request.user.is_paid:
                return JsonResponse(
                    {'error': 'Permission Denied. Please upgrade your account to access this feature.'}, status=status.HTTP_402_PAYMENT_REQUIRED)

        return self.get_response(request)

    def is_exempt_path(self, path, payment_exempt=False):
        # Check if the path matches any of the exempt patterns
        exempt_paths = settings.AUTH_EXEMPT_PATHS
        if payment_exempt:
            exempt_paths = settings.AUTH_EXEMPT_PATHS + settings.PAYMENT_EXEMPT_PATHS

        for pattern in exempt_paths:
            if re.match(pattern, path):
                return True
        return False
