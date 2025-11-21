# catalogo/urls.py
from django.urls import path
from .views import (
    ServiciosListView, PaquetesListView, BannersListView,
    ServicioDetailView, PaqueteDetailView
)

urlpatterns = [
    path("servicios/", ServiciosListView.as_view(), name="servicios-list"),
    path("servicios/<int:pk>/", ServicioDetailView.as_view(), name="servicio-detail"),
    path("paquetes/", PaquetesListView.as_view(), name="paquetes-list"),
    path("paquetes/<int:pk>/", PaqueteDetailView.as_view(), name="paquete-detail"),
    path("banners/", BannersListView.as_view(), name="banners-list"),
]
