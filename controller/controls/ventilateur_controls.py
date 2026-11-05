"""
Contrôles de ventilateur (allumer / éteindre)
"""

from hardware import relais
from controller.models import Ventilateur



def get_etat_ventilateur(ventilateur: Ventilateur):
    """
    Renvoie si le ventilateur est allumé ou non
    """

    ventilateur_device = relais(ventilateur.gpio_broche)
    return ventilateur_device.value


def commander_ventilateur(ventilateur: Ventilateur, requested_action: str):
    """
    Allume ou éteint un ventilateur donné
    """

    if requested_action not in ["on", "off"]:
        raise ValueError(f"requested_action doit être 'on' ou 'off'. Lu : {requested_action}")
        
    ventilateur_device = relais(ventilateur.gpio_broche)

    if requested_action == 'on':
        ventilateur_device.on()

    elif requested_action == 'off':
        ventilateur_device.off()
    


