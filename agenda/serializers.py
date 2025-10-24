from rest_framework import serializers
from .models import Barbero, DisponibilidadSemanal, Cita
from django.utils import timezone

class BarberoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barbero
        fields = ("id","nombre_mostrado","biografia","activo")

class DisponibilidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisponibilidadSemanal
        fields = "__all__"

class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = "__all__"
        read_only_fields = ("estado","cliente","fecha_hora_fin","creada_en")

    def validate(self, attrs):
        servicio = attrs["servicio"]
        inicio = attrs["fecha_hora_inicio"]
        attrs["fecha_hora_fin"] = inicio + timezone.timedelta(minutes=servicio.duracion_minutos)
        return attrs

    def create(self, datos):
        datos["cliente"] = self.context["request"].user
        return super().create(datos)

class ConsultaSlotsSerializer(serializers.Serializer):
    id_barbero = serializers.IntegerField()
    fecha = serializers.DateField()
    id_servicio = serializers.IntegerField()
