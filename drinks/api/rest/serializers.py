from rest_framework import serializers

from drinks.models import Drink, Ingredient


class DrinkSerializer(serializers.HyperlinkedModelSerializer):
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True, allow_empty=False, queryset=Ingredient.objects.all()
    )

    class Meta:
        model = Drink
        fields = ("id", "name", "ingredients")


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name")
