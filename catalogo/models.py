from django.db import models

class Servicio(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    duracion_minutos = models.PositiveIntegerField(default=30)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    activo = models.BooleanField(default=True)

    def __str__(self): return self.nombre

class Paquete(models.Model):
    titulo = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    servicios = models.ManyToManyField(Servicio, related_name="paquetes", blank=True)
    precio_promocional = models.DecimalField(max_digits=8, decimal_places=2)
    activo = models.BooleanField(default=True)

class BannerInicio(models.Model):
    titulo = models.CharField(max_length=120)
    imagen = models.ImageField(upload_to="banners/")
    enlace = models.URLField(blank=True)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)
