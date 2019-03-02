from rest_framework import viewsets

from drinks.api.rest.serializers import DrinkSerializer, IngredientSerializer
from drinks.models import Drink, Ingredient


class DrinkViewSet(viewsets.ModelViewSet):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
