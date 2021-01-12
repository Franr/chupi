from rest_framework import filters, viewsets

from drinks.api.rest.serializers import DrinkSerializer, DrinkWriteSerializer, IngredientSerializer
from drinks.models import Drink, Ingredient

WRITABLE_ACTIONS = ("update", "partial_update", "create")


class DrinkViewSet(viewsets.ModelViewSet):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name", "ingredients__name")

    def get_serializer_class(self):
        if self.action in WRITABLE_ACTIONS:
            return DrinkWriteSerializer
        return super().get_serializer_class()


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
