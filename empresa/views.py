
# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import ConfiguracionEmpresa
from .serializers import ConfiguracionEmpresaSerializer

class EmpresaViewSet(ModelViewSet):
    """
    /api/empresa/config/        -> GET (listar), POST (crear)
    /api/empresa/config/{id}/   -> GET (detalle), PATCH/PUT (editar), DELETE (eliminar)
    """
    queryset = ConfiguracionEmpresa.objects.all().order_by("id")
    serializer_class = ConfiguracionEmpresaSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_permissions(self):
        # Permitir lectura sin autenticación; escribir solo admin
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            return [AllowAny()]
        return [IsAdminUser()]
