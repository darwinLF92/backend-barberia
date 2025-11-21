from django.urls import path
from .views import RegistroView, confirmar_correo, crear_contrasena, PerfilView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("registro/", RegistroView.as_view(), name="registro"),
    path("confirmar-correo/", confirmar_correo, name="confirmar-correo"),
    path("crear-contrasena/", crear_contrasena, name="crear-contrasena"),
    path("perfil/", PerfilView.as_view(), name="perfil"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/actualizar/", TokenRefreshView.as_view(), name="token_refresh"),
]
