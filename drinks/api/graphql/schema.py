from typing import List

import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from drinks.api.graphql import DRINK_NOT_FOUND, INGREDIENT_NOT_FOUND, INGREDIENTS_EMPTY
from drinks.models import Container, Drink, Garnish, Ingredient, Technique


class ContainerType(DjangoObjectType):
    class Meta:
        model = Container


class GarnishType(DjangoObjectType):
    class Meta:
        model = Garnish


class TechniqueType(DjangoObjectType):
    class Meta:
        model = Technique


class DrinkType(DjangoObjectType):
    class Meta:
        model = Drink

    likes = graphene.Int(resolver=lambda d, _: d.likes)


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient


class Query(graphene.ObjectType):
    all_drinks = graphene.List(DrinkType)
    all_ingredients = graphene.List(IngredientType, id=graphene.Int())

    drink = graphene.Field(DrinkType, id=graphene.Int())
    ingredient = graphene.Field(IngredientType, id=graphene.Int())
    container = graphene.Field(ContainerType, id=graphene.Int())
    garnish = graphene.Field(GarnishType, id=graphene.Int())
    technique = graphene.Field(TechniqueType, id=graphene.Int())

    def resolve_all_drinks(self, info):
        return Drink.objects.all()

    def resolve_all_ingredients(self, info):
        return Ingredient.objects.all()

    def resolve_drink(self, info, **kwargs):
        drink_id = kwargs.get("id")

        if drink_id is not None:
            return Drink.objects.get(pk=drink_id)

    def resolve_ingredient(self, info, **kwargs):
        ingredient_id = kwargs.get("id")

        if ingredient_id is not None:
            return Ingredient.objects.get(pk=ingredient_id)


class CreateDrink(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        ingredients = graphene.List(graphene.Int)

    ok = graphene.Boolean()
    drink = graphene.Field(lambda: DrinkType)

    def mutate(self, info, name: str, ingredients: List[int]):
        if not ingredients:
            raise GraphQLError(INGREDIENTS_EMPTY)

        drink = Drink.objects.create(name=name)
        for ing in ingredients:
            drink.ingredients.add(ing)

        return CreateDrink(drink=drink, ok=True)


class UpdateDrink(graphene.Mutation):
    class Arguments:
        drink_id = graphene.Int()
        name = graphene.String()
        ingredients = graphene.List(graphene.Int)

    ok = graphene.Boolean()
    drink = graphene.Field(lambda: DrinkType)

    def mutate(self, info, drink_id: int, name: str, ingredients: List[int]):
        try:
            drink = Drink.objects.get(id=drink_id)
        except Drink.DoesNotExist:
            raise GraphQLError(DRINK_NOT_FOUND)

        if not ingredients:
            raise GraphQLError(INGREDIENTS_EMPTY)

        drink.name = name
        drink.ingredients.clear()
        for ing in ingredients:
            drink.ingredients.add(ing)
        drink.save()

        return UpdateDrink(drink=drink, ok=True)


class LikeDrink(graphene.Mutation):
    class Arguments:
        drink_id = graphene.Int()
        add = graphene.Boolean()

    ok = graphene.Boolean()
    likes = graphene.Int()
    add = graphene.Boolean()

    def mutate(self, info, drink_id: int, add: bool):
        try:
            drink = Drink.objects.get(id=drink_id)
        except Drink.DoesNotExist:
            raise GraphQLError(DRINK_NOT_FOUND)

        if add:
            total = drink.add_like()
        else:
            total = drink.remove_like()

        return LikeDrink(likes=total, add=add, ok=True)


class CreateIngredient(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    ingredient = graphene.Field(lambda: IngredientType)

    def mutate(self, info, name: str):
        ingredient = Ingredient.objects.create(name=name)

        return CreateIngredient(ingredient=ingredient, ok=True)


class UpdateIngredient(graphene.Mutation):
    class Arguments:
        ingredient_id = graphene.Int()
        name = graphene.String()

    ok = graphene.Boolean()
    ingredient = graphene.Field(lambda: IngredientType)

    def mutate(self, info, ingredient_id: int, name: str):
        try:
            ingredient = Ingredient.objects.get(id=ingredient_id)
        except Ingredient.DoesNotExist:
            raise GraphQLError(INGREDIENT_NOT_FOUND)

        ingredient.name = name
        ingredient.save()

        return CreateIngredient(ingredient=ingredient, ok=True)


class Mutation(graphene.ObjectType):
    create_drink = CreateDrink.Field()
    update_drink = UpdateDrink.Field()
    create_ingredient = CreateIngredient.Field()
    update_ingredient = UpdateIngredient.Field()
    like_drink = LikeDrink.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
