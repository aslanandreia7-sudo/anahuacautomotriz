from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("catalogo/", views.catalog, name="catalog"),
    path("catalogo/<slug:brand_slug>/", views.brand_catalog, name="brand_catalog"),
    path("catalogo/<slug:brand_slug>/<slug:model_slug>/", views.model_catalog, name="model_catalog"),
    path("auto/<slug:slug>/", views.car_detail, name="car_detail"),
    path("buscar/", views.search, name="search"),
    path("contacto/", views.contact, name="contact"),
]