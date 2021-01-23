from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from drinks.api.rest.serializers import (
    DrinkSerializer,
    DrinkWriteSerializer,
    IngredientSerializer,
    LikeSerializer,
    LikeWriteSerializer,
)
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

    @action(methods=["post"], detail=True, url_path="like", url_name="like")
    def like(self, request, **kwargs):
        drink = self.get_object()
        serializer = LikeWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.data["add"]:
            drink.add_like()
        else:
            drink.remove_like()

        return Response(LikeSerializer(instance=drink).data)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
