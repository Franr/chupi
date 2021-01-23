from django.urls import path

from drinks.views import DetailView, IndexView, generate_error_view, status_badge_view

drinks_templates_urlpatterns = (
    [
        path("drinks/<int:pk>/", DetailView.as_view(), name="detail"),
        path("drinks/", IndexView.as_view(), name="index"),
        path("generate_error/", generate_error_view, name="error"),
        path("status_badge/", status_badge_view, name="badge"),
    ],
    "drinks",
)
