from django.views.generic import ListView
from drinks.models import Drink

class DrinkList(ListView):
    model = Drink
