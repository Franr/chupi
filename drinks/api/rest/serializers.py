from rest_framework import serializers

from drinks.models import Drink, Ingredient


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name")


class DrinkSerializer(serializers.HyperlinkedModelSerializer):
    ingredients = IngredientSerializer(many=True, allow_empty=False)

    class Meta:
        model = Drink
        fields = ("id", "name", "ingredients")


class DrinkWriteSerializer(DrinkSerializer):
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True, allow_empty=False, queryset=Ingredient.objects.all()
    )
