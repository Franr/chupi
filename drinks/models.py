from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# TODO: apply this improvement when info available
class Measure(models.Model):
    amount = models.FloatField()
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


class Drink(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.name
