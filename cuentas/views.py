from rest_framework import generics, permissions, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import (
    RegistroSerializer, ConfirmarCorreoSerializer, CrearContrasenaSerializer
)

class RegistroView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegistroSerializer

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        if not ser.is_valid():
            print("❌ Registro errores:", ser.errors)  # <-- log temporal
            raise serializers.ValidationError(ser.errors)
        self.perform_create(ser)
        return Response(ser.data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def confirmar_correo(request):
    s = ConfirmarCorreoSerializer(data=request.data)
    if not s.is_valid():
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
    s.save()
    return Response({"detalle": "Correo confirmado."}, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def crear_contrasena(request):
    s = CrearContrasenaSerializer(data=request.data)
    if not s.is_valid():
        print("❌ crear_contrasena errores:", s.errors)  # temporal para ver el detalle en la consola
        raise serializers.ValidationError(s.errors)
    s.save()
    return Response({"detalle": "Contraseña creada. Ya puedes iniciar sesión."}, status=status.HTTP_200_OK)