"""
Point d'entrée matériel. Le reste du projet importe uniquement `relais` et `dht` d'ici.
Le backend est choisi par settings.HARDWARE_MODE ("fake" sur PC, "real" sur le Raspberry).
"""

from django.conf import settings

_MODE = getattr(settings, "HARDWARE_MODE", "fake")

if _MODE == "real":
    from .real import relais, dht
elif _MODE == "fake":
    from .fake import relais, dht
else:
    raise ValueError(f"HARDWARE_MODE doit être 'real' ou 'fake'. Lu : {_MODE!r}")

__all__ = ["relais", "dht"]
