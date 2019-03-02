from graphene_django import DjangoObjectType
import graphene

from drinks.models import Drink, Ingredient


class DrinkType(DjangoObjectType):
    class Meta:
        model = Drink


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient


class Query(graphene.ObjectType):
    drink = graphene.Field(DrinkType, id=graphene.Int())
    all_drinks = graphene.List(DrinkType)
    ingredient = graphene.Field(IngredientType, id=graphene.Int())
    all_ingredients = graphene.List(IngredientType, id=graphene.Int())

    def resolve_drink(self, info, **kwargs):
        drink_id = kwargs.get("id")

        if drink_id is not None:
            return Drink.objects.get(pk=drink_id)

    def resolve_all_drinks(self, info):
        return Drink.objects.all()

    def resolve_ingredient(self, info, **kwargs):
        ingredient_id = kwargs.get("id")

        if ingredient_id is not None:
            return Ingredient.objects.get(pk=ingredient_id)

    def resolve_all_ingredients(self, info):
        return Ingredient.objects.all()


schema = graphene.Schema(query=Query)
