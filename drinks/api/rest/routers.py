from rest_framework import routers

from drinks.api.rest.views import DrinkViewSet

drinks_router = routers.DefaultRouter()
drinks_router.register(r'drinks', DrinkViewSet)
