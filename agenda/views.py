from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Barbero, DisponibilidadSemanal, Cita
from .serializers import BarberoSerializer, DisponibilidadSerializer, CitaSerializer, ConsultaSlotsSerializer
from .services import generar_slots
from catalogo.models import Servicio
from notificaciones.services import notificar_cita_whatsapp

class SoloLecturaPublico(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET","HEAD","OPTIONS"):
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff

class BarberoViewSet(viewsets.ModelViewSet):
    queryset = Barbero.objects.filter(activo=True)
    serializer_class = BarberoSerializer
    permission_classes = [SoloLecturaPublico]

class DisponibilidadViewSet(viewsets.ModelViewSet):
    queryset = DisponibilidadSemanal.objects.all()
    serializer_class = DisponibilidadSerializer
    permission_classes = [permissions.IsAdminUser]

class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all().select_related("barbero","servicio","cliente")
    serializer_class = CitaSerializer

    def get_queryset(self):
        u = self.request.user
        return self.queryset if u.is_staff else self.queryset.filter(cliente=u)

    @action(detail=False, methods=["GET"], permission_classes=[permissions.AllowAny])
    def slots(self, request):
        s = ConsultaSlotsSerializer(data=request.query_params)
        s.is_valid(raise_exception=True)
        barbero = get_object_or_404(Barbero, pk=s.validated_data["id_barbero"], activo=True)
        servicio = get_object_or_404(Servicio, pk=s.validated_data["id_servicio"], activo=True)
        libres = generar_slots(barbero, s.validated_data["fecha"], servicio)
        return Response([dt.isoformat() for dt in libres])

    def perform_create(self, serializer):
        cita = serializer.save()
        try:
            notificar_cita_whatsapp(cita)
        except Exception:
            pass
