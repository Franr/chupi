from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from drinks.models import Drink, Ingredient
from drinks.api.rest.serializers import (
    DrinkSerializer,
    IngredientSerializer,
    DrinkWriteSerializer,
)


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
            {
                "id": 1,
                "name": "Whiscola",
                "ingredients": [
                    {"id": 1, "name": "Whisky"},
                    {"id": 2, "name": "Coca Cola"},
                ],
            },
        )

    def test_drink_deserializer(self):
        serializer = DrinkSerializer(
            data={"name": "Jameson", "ingredients": [{"name": self.whisky.name}]}
        )
        self.assertTrue(serializer.is_valid())

    def test_drink_empty_ingredients_validation(self):
        serializer = DrinkSerializer(data={"name": "Nothing", "ingredients": []})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["ingredients"]["non_field_errors"][0].code, "empty"
        )

    def test_drink_write_serializer(self):
        serializer = DrinkWriteSerializer(data={"name": "Empty", "ingredients": [self.whisky.id]})
        self.assertTrue(serializer.is_valid())

    def test_drink_write_deserializer(self):
        serializer = DrinkWriteSerializer(
            data={"name": "Water", "ingredients": [self.whisky.id]}
        )
        self.assertTrue(serializer.is_valid())

    def test_drink_write_empty_ingredients_validation(self):
        serializer = DrinkWriteSerializer(data={"name": "Empty", "ingredients": []})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["ingredients"][0].code, "empty"
        )

    def test_ingredient_serializer(self):
        self.assertDictEqual(
            IngredientSerializer(instance=self.whisky).data, {"id": 1, "name": "Whisky"}
        )

    def test_ingredient_deserializer(self):
        serializer = IngredientSerializer(data={"name": "water"})
        self.assertTrue(serializer.is_valid())


class ViewTests(APITestCase):
    def setUp(self):
        self.whisky = Ingredient.objects.create(name="Whisky")
        self.coca_cola = Ingredient.objects.create(name="Coca Cola")
        self.ice_cube = Ingredient.objects.create(name="Ice Cube")
        self.whiscola = Drink.objects.create(name="Whiscola")
        self.whiscola.ingredients.add(self.whisky, self.coca_cola)

    def test_get_drink(self):
        response = self.client.get(
            reverse("rest:rest-drinks-detail", args=(self.whiscola.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "name": "Whiscola",
                "ingredients": [
                    {"id": 1, "name": "Whisky"},
                    {"id": 2, "name": "Coca Cola"},
                ],
            },
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

    def test_update_drink(self):
        # auth
        user = get_user_model().objects.create_user("test", is_superuser=True)
        self.client.force_authenticate(user)
        # update
        url = reverse("rest:rest-drinks-detail", args=(self.whiscola.id,))
        data = {
            "name": "Whiscola with ice",
            "ingredients": [self.whisky.id, self.coca_cola.id, self.ice_cube.id],
        }
        response = self.client.put(url, data, format="json")
        # asserts
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Drink.objects.last().name, "Whiscola with ice")

    def test_partial_update_drink(self):
        # auth
        user = get_user_model().objects.create_user("test", is_superuser=True)
        self.client.force_authenticate(user)
        # partial update
        url = reverse("rest:rest-drinks-detail", args=(self.whiscola.id,))
        data = {"ingredients": [self.whisky.id]}
        response = self.client.patch(url, data, format="json")
        # asserts
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(Drink.objects.last().ingredients.all()), [self.whisky])

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
