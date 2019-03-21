from django.test import TestCase
from django.urls import reverse

from drinks import ERROR_MSG
from drinks.models import Drink, Ingredient


class UrlTests(TestCase):
    def setUp(self):
        self.whiscola = Drink.objects.create(name="Whiscola")

    def test_template_urls(self):
        self.assertEqual(reverse("template:index"), "/drinks/")
        self.assertEqual(
            reverse("template:detail", args=(self.whiscola.id,)), "/drinks/1/"
        )

    def test_error_url(self):
        self.assertEqual(reverse("template:error"), "/generate_error/")


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


class ErrorViewTests(TestCase):
    def test_error_view(self):
        url = reverse("template:error")
        self.assertRaisesMessage(Exception, ERROR_MSG, self.client.get, url)


class BadgeViewTests(TestCase):
    def test_error_view(self):
        url = reverse("template:badge")
        self.assertDictEqual(
            self.client.get(url).json(),
            {
                "schemaVersion": 1,
                "label": "server",
                "message": "running",
                "cacheSeconds": 60 * 60,
            },
        )
