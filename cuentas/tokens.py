# cuentas/tokens.py
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

_signer = TimestampSigner(salt="email-confirm-v1")

def make_email_token(user_id: int) -> str:
    # devuelve "valor:firmado" (string seguro para URL, y corto)
    return _signer.sign(str(user_id))

def read_email_token(token: str, max_age=60*60*24) -> int:
    # 24h por defecto
    unsigned = _signer.unsign(token, max_age=max_age)  # lanza si expira o es inválido
    return int(unsigned)
