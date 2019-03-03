from django.test import TestCase
from django.urls import reverse

from drinks.models import Drink, Ingredient


class UrlTests(TestCase):
    def setUp(self):
        self.whiscola = Drink.objects.create(name="Whiscola")

    def test_urls(self):
        self.assertEqual(reverse("template:index"), "/drinks/")
        self.assertEqual(
            reverse("template:detail", args=(self.whiscola.id,)), "/drinks/1/"
        )


class TemplateViewTests(TestCase):
    def setUp(self):
        self.whisky = Ingredient.objects.create(name="Whisky")
        self.coca_cola = Ingredient.objects.create(name="Coca Cola")
        self.whiscola = Drink.objects.create(name="Whiscola")
        self.whiscola.ingredients.add(self.whisky, self.coca_cola)

    def test_index(self):
        url = reverse("template:index")
        response = self.client.get(url)
        self.assertContains(response, self.whiscola.id)
        self.assertContains(response, self.whiscola.name)

    def test_detail(self):
        url = reverse("template:detail", args=(self.whiscola.id,))
        response = self.client.get(url)
        self.assertContains(response, self.whisky.name)
        self.assertContains(response, self.coca_cola.name)
        self.assertContains(response, self.whiscola.name)
