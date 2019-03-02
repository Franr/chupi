from rest_framework import serializers

from drinks.models import Drink, Ingredient


class DrinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Drink
        fields = ("id", "name")


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name")
