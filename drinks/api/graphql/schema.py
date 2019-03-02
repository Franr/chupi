from graphene_django import DjangoObjectType
import graphene
from graphql import GraphQLError

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


class CreateDrink(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        ingredients = graphene.List(graphene.Int)

    ok = graphene.Boolean()
    drink = graphene.Field(lambda: DrinkType)

    def mutate(self, info, name, ingredients):
        if not ingredients:
            raise GraphQLError("Ingredient list can't be empty")

        drink = Drink.objects.create(name=name)
        for ing in ingredients:
            drink.ingredients.add(ing)

        return CreateDrink(drink=drink, ok=True)


class CreateIngredient(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    ingredient = graphene.Field(lambda: IngredientType)

    def mutate(self, info, name):
        ingredient = Ingredient.objects.create(name=name)

        return CreateIngredient(ingredient=ingredient, ok=True)


class Mutation(graphene.ObjectType):
    create_drink = CreateDrink.Field()
    create_ingredient = CreateIngredient.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
