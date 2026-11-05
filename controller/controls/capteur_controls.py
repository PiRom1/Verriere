"""
Contrôles de capteurs (récupérer la température, l'humidité)
"""

from hardware import relais
from controller.models import Capteur
from hardware import dht
import time


def get_temperature_humidite(capteur: Capteur, essais = 5):
    """
    Récupère les valeurs de température et d'humidité d'un capteur donné
    """

    capteur = dht(capteur.gpio_broche)
    
    try:
        for _ in range(essais):
            try:
                t, h = capteur.temperature, capteur.humidity
                if t is not None and h is not None:
                    return t, h
            except RuntimeError:
                pass          # lecture ratée, normal avec un DHT22
            time.sleep(2)     # il faut 2 s mini entre deux lectures
    finally:
        capteur.exit()
    raise SystemError("Impossible de récupérer les informations de température et humidité")

