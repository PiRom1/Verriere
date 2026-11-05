"""
Informations de capteurs
"""

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from controller.models import Ventilateur, Capteur, Releve, CapteurMesure
from django.shortcuts import render, get_object_or_404, redirect
from controller.controls.capteur_controls import get_temperature_humidite
import json


def capteur(request, id):
    """
    Vue d'un capteur
    """

    capteur = get_object_or_404(Capteur, id=id)

    # Dernière mesure de CE capteur (un relevé peut ne pas en avoir si la lecture a échoué).
    derniere_mesure = (capteur.mesures
                       .select_related('releve')
                       .order_by('-releve__datetime')
                       .first())

    context = {
            'capteur' : capteur,
            'temperature' : derniere_mesure.temperature if derniere_mesure else None,
            'humidite' : derniere_mesure.humidite if derniere_mesure else None,
            'date_dernier_releve' : derniere_mesure.releve.datetime if derniere_mesure else None,
        }

    return render(request, 'controller/capteur/capteur.html', context)
    


def get_capteur_temperature_humidite(request):
    
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return HttpResponseBadRequest('<h1>400 Bad Request</h1><p>Requête non autorisée.</p>')

    payload = json.loads(request.body)
    print('payload : ', payload)
    capteur_id = int(payload['capteur_id'])
    capteur = get_object_or_404(Capteur, id = capteur_id)
    temperature, humidite = get_temperature_humidite(capteur = capteur)
    
    return JsonResponse({'success': True,
                         'data' : {'temperature' : temperature,
                                   'humidite' : humidite}})
