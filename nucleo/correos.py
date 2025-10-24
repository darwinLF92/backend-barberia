# nucleo/correos.py
from django.conf import settings
from django.core.mail import send_mail
from urllib.parse import urlencode

def enviar_correo(asunto, mensaje, para):
    if not para:
        raise ValueError("Destinatario vacío al enviar correo.")
    send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [para], fail_silently=False)

def enviar_confirmacion_correo(usuario, token):
    correo = getattr(usuario, "correo", None) or getattr(usuario, "email", None)
    if not correo:
        raise ValueError("El usuario no tiene correo.")

    # ✅ Construye el enlace aquí, sólo con params
    params = urlencode({"token": token, "correo": correo})
    enlace = f"{settings.FRONTEND_URL}/auth/confirmar?{params}"

    # Debug opcional
    print("DEBUG TOKEN  :", token)
    print("DEBUG ENLACE :", enlace)

    asunto = "Confirma tu cuenta - Barbería"
    mensaje = f"""
Hola {getattr(usuario, "nombres", "") or getattr(usuario, "username", "")},

Gracias por registrarte en Barbería 💈

Confirma tu correo y crea tu contraseña aquí:
{enlace}

Si no fuiste tú, ignora este mensaje.
"""
    enviar_correo(asunto, mensaje, correo)