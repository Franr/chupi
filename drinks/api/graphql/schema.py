from graphene_django import DjangoObjectType
import graphene

from drinks import models


class Drink(DjangoObjectType):
    class Meta:
        model = models.Drink


class Ingredient(DjangoObjectType):
    class Meta:
        model = models.Ingredient


class Query(graphene.ObjectType):
    drinks = graphene.List(Drink)
    ingredients = graphene.List(Ingredient)

    def resolve_drinks(self, info):
        return models.Drink.objects.all()

    def resolve_ingredients(self, info):
        return models.Ingredient.objects.all()


schema = graphene.Schema(query=Query)
