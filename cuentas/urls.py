from django.urls import path
from .views import RegistroView, confirmar_correo, crear_contrasena
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("registro/", RegistroView.as_view()),
    path("confirmar-correo/", confirmar_correo),
    path("crear-contrasena/", crear_contrasena),
    path("token/", TokenObtainPairView.as_view()),         # login JWT
    path("token/actualizar/", TokenRefreshView.as_view()), # refresh
]
