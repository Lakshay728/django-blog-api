import time
import logging

logger = logging.getLogger(__name__)

class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Before the view
        start_time = time.time()
        method = request.method
        path = request.path

        # Call the view
        response = self.get_response(request)

        # After the view
        duration = time.time() - start_time
        print(f'⏱️ {method} {path} → {response.status_code} ({duration:.2f}s)')

        return response


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.http import JsonResponse
        from django.conf import settings

        # Check if maintenance mode is on
        if getattr(settings, 'MAINTENANCE_MODE', False):
            # Allow admin through
            if not request.path.startswith('/admin'):
                return JsonResponse({
                    'message': 'Site is under maintenance. Please try again later!'
                }, status=503)

        return self.get_response(request)