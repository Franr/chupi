from django.core.cache import caches
from django.db import models
from django.db.models import SET_NULL

from drinks.utils import RedisKeyMixin

cache = caches["default"]


class NamedItem(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(self.name)


class Element(NamedItem):
    """
    - whisky
    - ron
    - vodka
    - ...
    """


class Measure(NamedItem):
    """
    - 60ml
    - 120ml
    - a dash
    - ...
    """


class Technique(NamedItem):
    """
    - direct
    - shacked
    - frozen
    - ...
    """


class Container(NamedItem):
    """
    - wine glass
    - long glass
    - whisky glass
    - ...
    """


class Garnish(NamedItem):
    """
    - mint
    - lemon skin
    - orange slice
    - ...
    """


class Ingredient(NamedItem):
    """
    An amount of an element:
    - whisky 60ml
    - orange juice 130ml
    - a dash of soda
    - ...
    """

    element = models.ForeignKey(Element, on_delete=SET_NULL, null=True, blank=True)
    measure = models.ForeignKey(Measure, on_delete=SET_NULL, null=True, blank=True)


class Drink(NamedItem, RedisKeyMixin):
    """
    A combination of all the previous models.
    """

    ingredients = models.ManyToManyField(Ingredient)
    garnish = models.ForeignKey(Garnish, on_delete=SET_NULL, null=True, blank=True)
    technique = models.ForeignKey(Technique, on_delete=SET_NULL, null=True, blank=True)
    container = models.ForeignKey(Container, on_delete=SET_NULL, null=True, blank=True)
    recipe = models.TextField(blank=True)

    @property
    def likes(self):
        total = cache.get(self.redis_key)
        return total and int(total) or 0

    def add_like(self):
        return int(cache.incr(self.redis_key))

    def remove_like(self):
        if self.likes <= 0:  # prevent negative likes
            return 0
        return int(cache.decr(self.redis_key))

    def _set_likes(self, amount):
        return int(cache.set(self.redis_key, amount))
