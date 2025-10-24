from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class Usuario(AbstractUser):
    cui = models.CharField("CUI", max_length=20, unique=True)
    nombres = models.CharField("Nombres", max_length=100)
    apellidos = models.CharField("Apellidos", max_length=100)
    direccion = models.CharField("Dirección", max_length=255, blank=True, null=True)
    fecha_nacimiento = models.DateField("Fecha de nacimiento", blank=True, null=True)
    estatura = models.DecimalField("Estatura (m)", max_digits=5, decimal_places=2, blank=True, null=True)
    telefono = models.CharField("Teléfono", max_length=20, blank=True, null=True)
    correo = models.EmailField("Correo electrónico", unique=True)
    correo_verificado = models.BooleanField("Correo verificado", default=False)
    estado = models.BooleanField("Activo", default=True)
    grupos = models.ManyToManyField(Group, verbose_name="Roles", blank=True, related_name="usuarios")

    USERNAME_FIELD = "correo"  # el login se hará con correo
    REQUIRED_FIELDS = ["username", "cui", "nombres", "apellidos"]

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.correo})"