from rest_framework import viewsets

from drinks.api.rest.serializers import DrinkSerializer
from drinks.models import Drink


class DrinkViewSet(viewsets.ModelViewSet):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer
