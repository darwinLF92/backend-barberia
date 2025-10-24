from django.db import models
from django.conf import settings

Usuario = settings.AUTH_USER_MODEL

class Barbero(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="perfil_barbero")
    nombre_mostrado = models.CharField(max_length=120)
    biografia = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    def __str__(self): return self.nombre_mostrado

class DisponibilidadSemanal(models.Model):
    # 0 = Lunes ... 6 = Domingo
    barbero = models.ForeignKey(Barbero, on_delete=models.CASCADE, related_name="disponibilidades")
    dia_semana = models.PositiveSmallIntegerField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    class Meta:
        unique_together = ("barbero","dia_semana","hora_inicio","hora_fin")

class Ausencia(models.Model):
    barbero = models.ForeignKey(Barbero, on_delete=models.CASCADE, related_name="ausencias")
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField()

class Cita(models.Model):
    ESTADOS = [
        ("PENDIENTE","Pendiente"),
        ("CONFIRMADA","Confirmada"),
        ("CANCELADA","Cancelada"),
        ("PROCESADA","Procesada"),
    ]
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="citas")
    barbero = models.ForeignKey(Barbero, on_delete=models.CASCADE, related_name="citas")
    servicio = models.ForeignKey("catalogo.Servicio", on_delete=models.PROTECT)
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField()
    estado = models.CharField(max_length=10, choices=ESTADOS, default="PENDIENTE")
    notas = models.CharField(max_length=255, blank=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("barbero","fecha_hora_inicio")
