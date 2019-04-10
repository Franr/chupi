from django.urls import path

from front_vue.views import FrontEndView

front_templates_urlpatterns = (
    [path("front/", FrontEndView.as_view(), name="vue")],
    "vue",
)
