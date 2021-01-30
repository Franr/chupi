from datetime import datetime

from django.core.cache import caches
from django.http import HttpResponse

cache = caches["default"]


class HttpThrottled(HttpResponse):
    status_code = 429


class GQLThrottlingMiddleware:
    THRESHOLD = 10
    PATH = "/api-graphql/"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith(self.PATH):
            return self.get_response(request)

        user_ip = request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get("REMOTE_ADDR")
        key = f"{user_ip}:{datetime.now().minute}"
        hits = cache.get(key)

        if hits and hits >= self.THRESHOLD:
            return HttpThrottled()
        elif hits is None:
            cache.set(key, 1, timeout=60)  # expire on 1 minute (our time-window)
        else:
            cache.incr(key)

        return self.get_response(request)
