from django.db import models

class ConfiguracionEmpresa(models.Model):
    nombre = models.CharField(max_length=120)
    nit = models.CharField(max_length=32, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    whatsapp_e164 = models.CharField(max_length=20, blank=True)
    logo = models.ImageField(upload_to="empresa/", blank=True, null=True)
    mensaje_inicio = models.TextField(blank=True)

    def __str__(self): return self.nombre
