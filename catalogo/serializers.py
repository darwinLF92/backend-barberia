from rest_framework import serializers
from .models import Servicio, Paquete, BannerInicio

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = "__all__"

class PaqueteSerializer(serializers.ModelSerializer):
    servicios = ServicioSerializer(many=True, read_only=True)
    ids_servicios = serializers.PrimaryKeyRelatedField(
        source="servicios", queryset=Servicio.objects.all(), many=True, write_only=True, required=False
    )
    class Meta:
        model = Paquete
        fields = ("id","titulo","descripcion","precio_promocional","activo","servicios","ids_servicios")

class BannerInicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerInicio
        fields = "__all__"
