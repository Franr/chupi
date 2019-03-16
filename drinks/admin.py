from django.contrib import admin

from drinks.models import Drink, Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    ordering = ("name",)
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    ordering = ("name",)
    list_display = ("id", "name")
    filter_horizontal = ("ingredients",)
    search_fields = ("name",)
