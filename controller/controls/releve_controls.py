"""
Écriture des relevés
"""

from controller.models import Releve, Ventilateur, VentilateurEtat, Capteur, CapteurMesure
from django.db import transaction 
from controller.controls.capteur_controls import get_temperature_humidite
from controller.controls.ventilateur_controls import get_etat_ventilateur


@transaction.atomic()
def ecrire_releve():
    """
    Ecrit un relevé daté : 
        - Température et humidité des capteurs
        - État des ventilateurs
    """

    # Relevé global
    releve = Releve.objects.create()
    erreurs = {}

    # États des ventilateurs
    ventilateurs_erreurs = {}
    for ventilateur in Ventilateur.objects.all():
        try:
            VentilateurEtat.objects.create(releve = releve,
                                           ventilateur = ventilateur,
                                           est_allume = get_etat_ventilateur(ventilateur))
        except Exception as e:
            ventilateurs_erreurs[ventilateur.id] = str(e)

    if ventilateurs_erreurs:
        erreurs['ventilateurs'] = ventilateurs_erreurs

    # Mesures des capteurs
    capteurs_erreurs = {}
    for capteur in Capteur.objects.all():

        try:
            temperature, humidite = get_temperature_humidite(capteur)

            CapteurMesure.objects.create(releve = releve,
                                         capteur = capteur,
                                         temperature = temperature,
                                         humidite = humidite)
        except Exception as e:
            capteurs_erreurs[capteur.id] = str(e)

    if capteurs_erreurs:
        erreurs['capteurs'] = capteurs_erreurs


    if erreurs:
        releve.erreurs = erreurs
        releve.save()

    print(f"Relevé écrit le {releve.datetime}")
    if erreurs:
        print("    - /!\\ Erreurs")
    
    
        


