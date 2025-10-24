from datetime import datetime, timedelta, time
from django.utils import timezone
from .models import DisponibilidadSemanal, Ausencia, Cita, Barbero
from catalogo.models import Servicio

def generar_slots(barbero: Barbero, fecha, servicio: Servicio, minutos_slot: int = 15):
    tz = timezone.get_current_timezone()
    weekday = fecha.weekday()  # 0..6
    bloques = DisponibilidadSemanal.objects.filter(barbero=barbero, dia_semana=weekday)
    if not bloques.exists():
        return []

    dia_ini = tz.localize(datetime.combine(fecha, time(0,0)))
    dia_fin = dia_ini + timedelta(days=1)

    ocupadas = []
    for s,e in Cita.objects.filter(
        barbero=barbero, fecha_hora_inicio__gte=dia_ini, fecha_hora_inicio__lt=dia_fin
    ).exclude(estado="CANCELADA").values_list("fecha_hora_inicio","fecha_hora_fin"):
        ocupadas.append((s.astimezone(tz), e.astimezone(tz)))

    for off in Ausencia.objects.filter(barbero=barbero, fecha_hora_fin__gt=dia_ini, fecha_hora_inicio__lt=dia_fin):
        ocupadas.append((off.fecha_hora_inicio.astimezone(tz), off.fecha_hora_fin.astimezone(tz)))

    dur = timedelta(minutes=servicio.duracion_minutos)
    paso = timedelta(minutes=minutos_slot)

    libres = []
    for b in bloques:
        cursor = tz.localize(datetime.combine(fecha, b.hora_inicio))
        fin_b = tz.localize(datetime.combine(fecha, b.hora_fin))
        while cursor + dur <= fin_b:
            ini = cursor
            fin = cursor + dur
            conflicto = any(not (fin <= s or ini >= e) for s, e in ocupadas)
            if not conflicto and ini > timezone.now():
                libres.append(ini)
            cursor += paso
    return sorted(libres)
