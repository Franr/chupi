import factory
from factory.django import DjangoModelFactory

from drinks import models


class ContainerFactory(DjangoModelFactory):
    class Meta:
        model = models.Container


class GarnishFactory(DjangoModelFactory):
    class Meta:
        model = models.Garnish


class TechniqueFactory(DjangoModelFactory):
    class Meta:
        model = models.Technique


class ElementFactory(DjangoModelFactory):
    class Meta:
        model = models.Element


class MeasureFactory(DjangoModelFactory):
    class Meta:
        model = models.Measure


class IngredientFactory(DjangoModelFactory):
    class Meta:
        model = models.Ingredient

    element = factory.SubFactory(ElementFactory)
    measure = factory.SubFactory(MeasureFactory)


class DrinkFactory(DjangoModelFactory):
    class Meta:
        model = models.Drink

    garnish = factory.SubFactory(GarnishFactory)
    technique = factory.SubFactory(TechniqueFactory)
    container = factory.SubFactory(ContainerFactory)

    @factory.post_generation
    def ingredients(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for ingredient in extracted:
                self.ingredients.add(ingredient)
