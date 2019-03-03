"""chupi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from drinks.api.rest.routers import rest_urlpatterns
from drinks.api.graphql.urls import graphql_urlpatterns
from drinks.urls import drinks_templates_urlpatterns

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Template views
    path("", include(drinks_templates_urlpatterns, namespace="template")),
    # Rest API
    path("api-auth/", include("rest_framework.urls")),
    path("api-rest/", include(rest_urlpatterns, namespace="rest")),
    # GraphQL API
    path("api-graphql/", include(graphql_urlpatterns)),
]
