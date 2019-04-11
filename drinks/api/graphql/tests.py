import json

from django.test import TestCase
from django.urls import reverse
from graphql import GraphQLError

from drinks.api.graphql import INGREDIENTS_EMPTY, DRINK_NOT_FOUND, INGREDIENT_NOT_FOUND
from drinks.api.graphql.schema import CreateDrink, UpdateDrink, UpdateIngredient
from drinks.factories import GinTonicFactory, IngredientFactory, DrinkFactory
from drinks.models import Drink, Ingredient


class UrlTests(TestCase):
    def test_drink_urls(self):
        self.assertEqual(reverse("graphql:api"), "/api-graphql/")


class SchemaMutationsValidationsTests(TestCase):
    def setUp(self):
        self.whisky = Ingredient.objects.create(name="Whisky")
        self.coca_cola = Ingredient.objects.create(name="Coca Cola")
        self.whiscola = Drink.objects.create(name="Whiscola")
        self.whiscola.ingredients.add(self.whisky, self.coca_cola)

    def test_create_drink_empty_ingredients_validation(self):
        drink_schema = CreateDrink()
        self.assertRaisesMessage(
            GraphQLError,
            INGREDIENTS_EMPTY,
            drink_schema.mutate,
            None,
            "Fernet Cola",
            [],
        )

    def test_update_drink_empty_ingredients_validation(self):
        drink_schema = UpdateDrink()
        self.assertRaisesMessage(
            GraphQLError,
            INGREDIENTS_EMPTY,
            drink_schema.mutate,
            None,
            self.whiscola.id,
            "Whisky Jameson",
            [],
        )

    def test_update_drink_wrong_id_validation(self):
        drink_schema = UpdateDrink()
        bad_id = 1000
        self.assertRaisesMessage(
            GraphQLError,
            DRINK_NOT_FOUND,
            drink_schema.mutate,
            None,
            bad_id,
            "Whisky Jameson",
            [],
        )

    def test_update_ingredient_wrong_id_validation(self):
        drink_schema = UpdateIngredient()
        bad_id = 1000
        self.assertRaisesMessage(
            GraphQLError,
            INGREDIENT_NOT_FOUND,
            drink_schema.mutate,
            None,
            bad_id,
            "Water",
        )


class QueryAPI(TestCase):
    api_url = reverse("graphql:api")

    def query(self, query, variables=None):
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        response = self.client.post(
            self.api_url, json.dumps(payload), content_type="application/json"
        )
        return response.json()


class APIQueriesTestCase(QueryAPI):
    def setUp(self):
        self.gin_tonic = GinTonicFactory()

    def test_all_drinks(self):
        query = """
        query {
            allDrinks {
                id
            }
        }
        """
        self.assertEqual(
            self.query(query, variables={"id": self.gin_tonic.id}),
            {"data": {"allDrinks": [{"id": "1"}]}},
        )

    def test_get_drink(self):
        query = """
        query ($id: Int) {
            drink(id:$id) {
                id
                name
                ingredients {
                    id
                    name
                }
                garnish {
                    name
                }
                technique {
                    name
                }
                container {
                    name
                }
            }
        }
        """
        self.maxDiff = None
        self.assertEqual(
            self.query(query, variables={"id": self.gin_tonic.id}),
            {
                "data": {
                    "drink": {
                        "id": "1",
                        "name": "Gin Tonic",
                        "ingredients": [
                            {"id": "1", "name": "Gin 60ml"},
                            {"id": "2", "name": "Tonic Soda 140ml"},
                        ],
                        "garnish": {"name": "Lemon Slice"},
                        "technique": {"name": "Direct"},
                        "container": {"name": "Balloon Glass"},
                    }
                }
            },
        )

    def test_all_ingredients(self):
        query = """
        query {
            allIngredients {
                id
            }
        }
        """
        self.assertEqual(
            self.query(query, variables={"id": self.gin_tonic.id}),
            {"data": {"allIngredients": [{"id": "1"}, {"id": "2"}]}},
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
            self.query(query, variables={"id": self.gin_tonic.ingredients.first().id}),
            {"data": {"ingredient": {"id": "1", "name": "Gin 60ml"}}},
        )


class APIMutationsTestCase(QueryAPI):
    def setUp(self):
        self.whisky = IngredientFactory(name="Whisky")
        self.ice_cube = IngredientFactory(name="Ice Cube")
        self.coca_cola = IngredientFactory(name="Coca Cola")
        self.whiscola = DrinkFactory(ingredients=(self.whisky, self.coca_cola))

    def test_create_drink(self):
        query = """
        mutation ($name: String, $ingredients: [Int]) {
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
                                {"id": "2", "name": "Ice Cube"},
                            ],
                        },
                    }
                }
            },
        )

    def test_update_drink(self):
        query = """
        mutation ($drink_id: Int, $name: String, $ingredients: [Int]) {
            updateDrink(drinkId: $drink_id, name: $name, ingredients: $ingredients) {
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

        self.assertEqual(
            self.query(
                query,
                variables={
                    "drink_id": self.whiscola.id,
                    "name": "Whiscola on the rock",
                    "ingredients": [
                        self.whisky.id,
                        self.ice_cube.id,
                        self.coca_cola.id,
                    ],
                },
            ),
            {
                "data": {
                    "updateDrink": {
                        "ok": True,
                        "drink": {
                            "id": "1",
                            "name": "Whiscola on the rock",
                            "ingredients": [
                                {"id": "1", "name": "Whisky"},
                                {"id": "2", "name": "Ice Cube"},
                                {"id": "3", "name": "Coca Cola"},
                            ],
                        },
                    }
                }
            },
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

    def test_update_ingredient(self):
        query = """
        mutation ($ingredient_id: Int, $name: String) {
            updateIngredient(ingredientId: $ingredient_id, name: $name) {
                ok,
                ingredient {
                    id,
                    name
                }
            }
        }
        """
        self.assertEqual(
            self.query(
                query,
                variables={"ingredient_id": self.whisky.id, "name": "Whisky Jamenson"},
            ),
            {
                "data": {
                    "updateIngredient": {
                        "ok": True,
                        "ingredient": {"id": "1", "name": "Whisky Jamenson"},
                    }
                }
            },
        )
