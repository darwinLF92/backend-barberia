# catalogo/views.py
from rest_framework.generics import ListAPIView
from .models import Servicio, Paquete, BannerInicio
from .serializers import ServicioSerializer, PaqueteSerializer, BannerInicioSerializer
from rest_framework.permissions import AllowAny

class ServiciosListView(ListAPIView):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [AllowAny]   # 👈 público

class PaquetesListView(ListAPIView):
    queryset = Paquete.objects.all()
    serializer_class = PaqueteSerializer
    permission_classes = [AllowAny]   # 👈 público

class BannersListView(ListAPIView):
    queryset = BannerInicio.objects.all()
    serializer_class = BannerInicioSerializer
    permission_classes = [AllowAny]   # 👈 público