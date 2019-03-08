import json

from django.test import TestCase
from django.urls import reverse


from drinks.models import Drink, Ingredient


class UrlTests(TestCase):
    def test_drink_urls(self):
        self.assertEqual(reverse("graphql:api"), "/api-graphql/")


class APITestCase(TestCase):
    def setUp(self):
        self.api_url = reverse("graphql:api")
        self.whisky = Ingredient.objects.create(name="Whisky")
        self.coca_cola = Ingredient.objects.create(name="Coca Cola")
        self.ice_cube = Ingredient.objects.create(name="Ice Cube")
        self.whiscola = Drink.objects.create(name="Whiscola")
        self.whiscola.ingredients.add(self.whisky, self.coca_cola)

    def query(self, query, variables=None):
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        response = self.client.post(
            self.api_url, json.dumps(payload), content_type="application/json"
        )
        return response.json()

    def test_get_drink(self):
        query = """
        query ($id: Int) {
            drink(id:$id) {
                id,
                name,
                ingredients {
                    id,
                    name
                }
            }
        }
        """
        self.assertEqual(
            self.query(query, variables={"id": self.whiscola.id}),
            {
                "data": {
                    "drink": {
                        "id": "1",
                        "name": "Whiscola",
                        "ingredients": [
                            {"id": "1", "name": "Whisky"},
                            {"id": "2", "name": "Coca Cola"},
                        ],
                    }
                }
            },
        )

    def test_create_drink(self):
        query = """
        mutation ($name: String, $ingredients: [Int]){
            createDrink(name: $name, ingredients: $ingredients) {
                ok,
                drink {
                    id,
                    name,
                    ingredients {
                        id,
                        name
                    }
                }
            }
        }
        """
        self.maxDiff = None
        self.assertEqual(
            self.query(
                query,
                variables={
                    "name": "Whisky on the rock",
                    "ingredients": [self.whisky.id, self.ice_cube.id],
                },
            ),
            {
                "data": {
                    "createDrink": {
                        "ok": True,
                        "drink": {
                            "id": "2",
                            "name": "Whisky on the rock",
                            "ingredients": [
                                {"id": "1", "name": "Whisky"},
                                {"id": "3", "name": "Ice Cube"},
                            ],
                        },
                    }
                }
            },
        )

    def test_get_ingredient(self):
        query = """
        query ($id: Int) {
            ingredient(id:$id) {
                id,
                name
            }
        }
        """
        self.assertEqual(
            self.query(query, variables={"id": self.whisky.id}),
            {"data": {"ingredient": {"id": "1", "name": "Whisky"}}},
        )

    def test_create_ingredient(self):
        query = """
        mutation ($name: String) {
            createIngredient(name: $name) {
                ok,
                ingredient {
                    id,
                    name
                }
            }
        }
        """
        self.assertEqual(
            self.query(query, variables={"name": "Vodka"}),
            {
                "data": {
                    "createIngredient": {
                        "ok": True,
                        "ingredient": {"id": "4", "name": "Vodka"},
                    }
                }
            },
        )
