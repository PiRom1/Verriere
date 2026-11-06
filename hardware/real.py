"""
Backend matériel réel : relais via gpiozero, capteurs DHT22 via adafruit_dht.
À n'importer que sur le Raspberry Pi (HARDWARE_MODE = "real").
"""

from gpiozero import OutputDevice
import adafruit_dht
import board

_devices = {}


def relais(gpio):
    if gpio not in _devices:
        _devices[gpio] = OutputDevice(gpio, active_high=False, initial_value=False)
    return _devices[gpio]


def dht(gpio):
    # Pas de cache : l'appelant termine chaque lecture par exit(), qui tue le
    # sous-processus de lecture des impulsions et rend l'objet inutilisable.
    return adafruit_dht.DHT22(getattr(board, f"D{gpio}"))
