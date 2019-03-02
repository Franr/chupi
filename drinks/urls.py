from django.urls import path

from drinks.views import DrinkList

drinks_templates_urlpatterns = [
    path('drinks/', DrinkList.as_view()),
]
