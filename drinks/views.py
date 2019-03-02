from django.views.generic import ListView, DetailView
from drinks.models import Drink


class DrinkList(ListView):
    model = Drink


class DrinkDetailView(DetailView):
    model = Drink