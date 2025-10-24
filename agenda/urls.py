from rest_framework.routers import DefaultRouter
from .views import BarberoViewSet, DisponibilidadViewSet, CitaViewSet

router = DefaultRouter()
router.register("barberos", BarberoViewSet)
router.register("disponibilidad", DisponibilidadViewSet)
router.register("citas", CitaViewSet)

urlpatterns = router.urls
