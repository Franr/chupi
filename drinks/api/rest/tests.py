from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from drinks.models import Drink, Ingredient
from drinks.api.rest.serializers import DrinkSerializer, IngredientSerializer


class UrlTests(TestCase):
    def setUp(self):
        self.whiscola = Drink.objects.create(name="Whiscola")
        self.coca_cola = Ingredient.objects.create(name="Coca Cola")

    def test_drink_urls(self):
        self.assertEqual(reverse("rest:rest-drinks-list"), "/api-rest/drinks/")
        self.assertEqual(
            reverse("rest:rest-drinks-detail", args=(self.whiscola.id,)),
            "/api-rest/drinks/1/",
        )

    def test_ingredients_urls(self):
        self.assertEqual(
            reverse("rest:rest-ingredients-list"), "/api-rest/ingredients/"
        )
        self.assertEqual(
            reverse("rest:rest-ingredients-detail", args=(self.whiscola.id,)),
            "/api-rest/ingredients/1/",
        )


class SerializersTests(TestCase):
    def setUp(self):
        self.whisky = Ingredient.objects.create(name="Whisky")
        self.coca_cola = Ingredient.objects.create(name="Coca Cola")
        self.whiscola = Drink.objects.create(name="Whiscola")
        self.whiscola.ingredients.add(self.whisky, self.coca_cola)

    def test_drink_serializer(self):
        self.assertDictEqual(
            DrinkSerializer(instance=self.whiscola).data,
            {"id": 1, "name": "Whiscola", "ingredients": [1, 2]},
        )

    def test_ingredient_serliazer(self):
        self.assertDictEqual(
            IngredientSerializer(instance=self.whisky).data, {"id": 1, "name": "Whisky"}
        )


class ViewTests(APITestCase):
    def setUp(self):
        self.whisky = Ingredient.objects.create(name="Whisky")
        self.coca_cola = Ingredient.objects.create(name="Coca Cola")
        self.whiscola = Drink.objects.create(name="Whiscola")
        self.whiscola.ingredients.add(self.whisky, self.coca_cola)

    def test_get_drink(self):
        response = self.client.get(
            reverse("rest:rest-drinks-detail", args=(self.whiscola.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), {"id": 1, "name": "Whiscola", "ingredients": [1, 2]}
        )

    def test_create_drink(self):
        # auth
        user = get_user_model().objects.create_user("test", is_superuser=True)
        self.client.force_authenticate(user)
        # create
        url = reverse("rest:rest-drinks-list")
        data = {"name": "Whisky on the rock", "ingredients": [self.whisky.id]}
        response = self.client.post(url, data, format="json")
        # asserts
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Drink.objects.last().name, "Whisky on the rock")

    def test_create_drink_empty_ingredients(self):
        # auth
        user = get_user_model().objects.create_user("test", is_superuser=True)
        self.client.force_authenticate(user)
        # create
        url = reverse("rest:rest-drinks-list")
        data = {"name": "Whisky on the rock", "ingredients": []}
        response = self.client.post(url, data, format="json")
        # asserts
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"ingredients": ["This list may not be empty."]}
        )

    def test_get_ingredient(self):
        response = self.client.get(
            reverse("rest:rest-ingredients-detail", args=(self.whisky.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"id": 1, "name": "Whisky"})

    def test_create_ingredient(self):
        # auth
        user = get_user_model().objects.create_user("test", is_superuser=True)
        self.client.force_authenticate(user)
        # create
        url = reverse("rest:rest-ingredients-list")
        data = {"name": "Vodka"}
        response = self.client.post(url, data, format="json")
        # asserts
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ingredient.objects.last().name, "Vodka")
