from django.urls import path

from drinks.views import IndexView, DetailView

drinks_templates_urlpatterns = (
    [
        path("drinks/<int:pk>/", DetailView.as_view(), name="detail"),
        path("drinks/", IndexView.as_view(), name="index"),
    ],
    "drinks",
)
