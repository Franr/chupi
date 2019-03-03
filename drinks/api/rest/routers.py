from django.urls import path, include
from rest_framework import routers

from drinks.api.rest.views import DrinkViewSet, IngredientViewSet

drinks_router = routers.DefaultRouter()
drinks_router.register("drinks", DrinkViewSet, base_name="rest-drinks")
drinks_router.register("ingredients", IngredientViewSet, base_name="rest-ingredients")


rest_urlpatterns = ([path("", include(drinks_router.urls))], "drinks")
