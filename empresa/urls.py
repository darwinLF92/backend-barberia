from rest_framework.routers import DefaultRouter
from .views import EmpresaViewSet

router = DefaultRouter()
router.register(r"config", EmpresaViewSet, basename="empresa")
urlpatterns = router.urls
