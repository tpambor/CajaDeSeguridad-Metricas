# Type hints para la FachadaCajaDeSeguridad

from typing import TypedDict

TipoClaveFavorita = TypedDict(
    'ClaveFavorita', {'nombre': str, 'clave': str, 'pista': str})
TipoElemento = TypedDict('Elemento', {
    'nombre_elemento': str, 'tipo': str, 'notas': str, # Login, Identificación, Tarjeta
    'clave': str,  # Login, Tarjeta, Secreto
    'email': str, 'usuario': str, 'url': str,  # Login
    'numero': str, 'fecha_venc': str,  # Identificación, Tarjeta
    'nombre': str, 'fecha_nacimiento': str, 'fecha_exp': str,  # Identificación
    'titular': str, 'ccv': int, 'direccion': str, 'telefono': str,  # Tarjeta
    'secreto': str,  # Secreto
}, total=False)

TipoReporte = TypedDict('Reporte', {
    'logins': int,
    'ids': int,
    'tarjetas': int,
    'secretos': int,
    'inseguras': int,
    'avencer': int,
    'masdeuna': int,
    'nivel': float,
})
