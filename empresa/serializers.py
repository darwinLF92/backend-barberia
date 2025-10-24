from rest_framework import serializers
from .models import ConfiguracionEmpresa

class ConfiguracionEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionEmpresa
        fields = "__all__"   # id, nombre, nit, direccion, telefono, whatsapp_e164, logo, mensaje_inicio

