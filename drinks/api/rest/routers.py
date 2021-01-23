from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from drinks.api.rest.views import DrinkViewSet, IngredientViewSet

drinks_router = routers.DefaultRouter()
drinks_router.register("drinks", DrinkViewSet, base_name="rest-drinks")
drinks_router.register("ingredients", IngredientViewSet, base_name="rest-ingredients")


rest_urlpatterns = (
    [
        path("", include(drinks_router.urls)),
        path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
        path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    ],
    "drinks",
)
