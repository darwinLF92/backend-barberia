from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from .tokens import make_email_token, read_email_token
from nucleo.correos import enviar_confirmacion_correo
from django.core.signing import BadSignature, SignatureExpired

Usuario = get_user_model()


class RegistroSerializer(serializers.ModelSerializer):
    # Mapea “usuario” → username del AbstractUser
    usuario = serializers.CharField(
        source="username",
        validators=[UniqueValidator(
            queryset=Usuario.objects.all(),
            message="Este nombre de usuario ya está en uso."
        )]
    )

    # Tu campo real de login es “correo”
    correo = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=Usuario.objects.all(),
            message="Este correo ya está registrado."
        )]
    )

    # Tipos/validaciones de tus campos
    fecha_nacimiento = serializers.DateField(required=False, allow_null=True, input_formats=["%Y-%m-%d", "%d/%m/%Y"])
    #estatura = serializers.DecimalField(max_digits=4, decimal_places=2, required=False, allow_null=True)

    class Meta:
        model = Usuario
        fields = (
            "cui", "usuario", "nombres", "apellidos", "direccion",
            "fecha_nacimiento", "estatura", "telefono", "correo"
        )

    def create(self, v):
        try:
            with transaction.atomic():
                u = Usuario.objects.create(
                    username=v.get("username"),
                    cui=v.get("cui", ""),
                    nombres=v.get("nombres", ""),
                    apellidos=v.get("apellidos", ""),
                    direccion=v.get("direccion", "") or "",
                    fecha_nacimiento=v.get("fecha_nacimiento"),
                    estatura=v.get("estatura"),
                    telefono=v.get("telefono", "") or "",
                    correo=v.get("correo"),
                    correo_verificado=False,
                    estado=True,
                    is_active=True,
                )
        except IntegrityError:
            raise serializers.ValidationError({"correo": "Este correo ya está registrado."})

        # ✅ Genera solo el token y pásalo sin tocar
        token = make_email_token(u.id)

        # ❌ NO construir aquí el enlace
        # enlace = f"{settings.FRONTEND_URL}/auth/confirmar?token={token}"

        # ✅ Deja que la función de correo lo construya correctamente
        transaction.on_commit(lambda: enviar_confirmacion_correo(u, token))
        return u


class ConfirmarCorreoSerializer(serializers.Serializer):
    token = serializers.CharField()

    def save(self, **kwargs):
        token = self.validated_data["token"]
        try:
            user_id = read_email_token(token)  # puede lanzar
        except SignatureExpired:
            raise serializers.ValidationError({"detalle": "El enlace ha expirado, solicita uno nuevo."})
        except BadSignature:
            raise serializers.ValidationError({"detalle": "Token inválido."})

        try:
            u = Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError({"detalle": "Usuario no encontrado."})

        u.correo_verificado = True
        u.save(update_fields=["correo_verificado"])
        return u


class CrearContrasenaSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    # acepta password “único” o doble confirmación
    password = serializers.CharField(write_only=True, required=False, allow_blank=True, min_length=6)
    password1 = serializers.CharField(write_only=True, required=False, allow_blank=True, min_length=6)
    password2 = serializers.CharField(write_only=True, required=False, allow_blank=True, min_length=6)

    def validate(self, attrs):
        # normaliza: decide qué password usar según lo que venga
        pwd = attrs.get("password")
        p1 = attrs.get("password1")
        p2 = attrs.get("password2")

        if not pwd and not p1:
            raise serializers.ValidationError({"password": "Debes enviar 'password' o 'password1/password2'."})

        if p1 is not None:  # usaron doble
            if p1 != p2:
                raise serializers.ValidationError({"password2": "Las contraseñas no coinciden."})
            pwd = p1

        # ejecuta validadores de Django
        validate_password(pwd)
        attrs["password_final"] = pwd
        return attrs

    def save(self, **kwargs):
        correo = self.validated_data["correo"]
        pwd = self.validated_data["password_final"]

        try:
            u = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError({"correo": "Usuario no encontrado."})

        if not u.correo_verificado:
            raise serializers.ValidationError({"detalle": "Debes confirmar tu correo antes de crear la contraseña."})

        u.set_password(pwd)  # maneja hash seguro
        u.save(update_fields=["password"])
        return u