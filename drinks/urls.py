from django.urls import path

from drinks.views import IndexView, DetailView, generate_error_view

drinks_templates_urlpatterns = (
    [
        path("drinks/<int:pk>/", DetailView.as_view(), name="detail"),
        path("drinks/", IndexView.as_view(), name="index"),
        path("generate_error/", generate_error_view, name="error"),
    ],
    "drinks",
)
