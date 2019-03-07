from django.urls import path
from graphene_django.views import GraphQLView

graphql_urlpatterns = (
    [path("", GraphQLView.as_view(graphiql=True), name="api")],
    "drinks",
)
