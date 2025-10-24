# catalogo/urls.py
from django.urls import path
from .views import ServiciosListView, PaquetesListView, BannersListView

urlpatterns = [
    path("servicios/", ServiciosListView.as_view()),
    path("paquetes/", PaquetesListView.as_view()),
    path("banners/", BannersListView.as_view()),
]
