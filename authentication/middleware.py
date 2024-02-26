from django.http import JsonResponse
from django.conf import settings
from rest_framework.authtoken.models import Token


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the requested path is exempt from authentication
        if request.path in settings.AUTH_EXEMPT_PATHS:
            return self.get_response(request)

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

        return self.get_response(request)
