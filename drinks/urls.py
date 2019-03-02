from django.urls import path

from drinks.views import DrinkList, DrinkDetailView

drinks_templates_urlpatterns = [
    path("drinks/<int:pk>/", DrinkDetailView.as_view(), name="drink-detail"),
    path("drinks/", DrinkList.as_view()),
]
