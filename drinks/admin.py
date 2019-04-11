from django.contrib import admin

from drinks import models


class NamedItemAdmin(admin.ModelAdmin):
    ordering = ("name",)
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(models.Element)
class ElementAdmin(NamedItemAdmin):
    pass


@admin.register(models.Measure)
class MeasureAdmin(NamedItemAdmin):
    pass


@admin.register(models.Technique)
class PreparationMethodAdmin(NamedItemAdmin):
    pass


@admin.register(models.Container)
class ContainerAdmin(NamedItemAdmin):
    pass


@admin.register(models.Garnish)
class GarnishAdmin(NamedItemAdmin):
    pass


@admin.register(models.Ingredient)
class IngredientAdmin(NamedItemAdmin):
    pass


@admin.register(models.Drink)
class DrinkAdmin(NamedItemAdmin):
    filter_horizontal = ("ingredients",)
