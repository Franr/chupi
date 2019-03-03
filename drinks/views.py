from django.views import generic
from drinks.models import Drink


class IndexView(generic.ListView):
    model = Drink


class DetailView(generic.DetailView):
    model = Drink
