from django.contrib import admin

from drinks.models import Drink, Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    ordering = ("name",)
    list_display = ("id", "name")


@admin.register(Drink)
class IngredientAdmin(admin.ModelAdmin):
    ordering = ("name",)
    list_display = ("id", "name")
    filter_horizontal = ("ingredients",)
