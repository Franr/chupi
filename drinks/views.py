from django.http import JsonResponse
from django.views import generic

from drinks import ERROR_MSG
from drinks.models import Drink


class IndexView(generic.ListView):
    model = Drink


class DetailView(generic.DetailView):
    model = Drink


def generate_error_view(request):
    raise Exception(ERROR_MSG)


def status_badge_view(request):
    data = {
        "schemaVersion": 1,
        "label": "server",
        "message": "running",
        "cacheSeconds": 60 * 60,
    }
    return JsonResponse(data)
