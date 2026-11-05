"""
Informations de capteurs
"""

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from controller.models import Ventilateur, Capteur, Releve
from django.shortcuts import render, get_object_or_404, redirect
from hardware import relais
from controller.controls.ventilateur_controls import commander_ventilateur, get_etat_ventilateur
import json


def ventilateur(request, id):
    """
    Vue d'un ventilateur
    """

    ventilateur = get_object_or_404(Ventilateur, id=id)
    ventilateur_est_allume = get_etat_ventilateur(ventilateur)
    

    context = {
            'ventilateur' : ventilateur,
            'ventilateur_est_allume' : ventilateur_est_allume
        }
        
    return render(request, 'controller/ventilateur/ventilateur.html', context)




def allumer_ventilateur(request):
    
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return HttpResponseBadRequest('<h1>400 Bad Request</h1><p>Requête non autorisée.</p>')

    payload = json.loads(request.body)
    ventilateur_id = int(payload['ventilateur_id'])
    ventilateur = get_object_or_404(Ventilateur, id = ventilateur_id)

    commander_ventilateur(ventilateur=ventilateur, requested_action='on')
    
    return JsonResponse({'success': True})



def eteindre_ventilateur(request):
    
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return HttpResponseBadRequest('<h1>400 Bad Request</h1><p>Requête non autorisée.</p>')
    
    payload = json.loads(request.body)
    ventilateur_id = int(payload['ventilateur_id'])
    ventilateur = get_object_or_404(Ventilateur, id = ventilateur_id)

    commander_ventilateur(ventilateur=ventilateur, requested_action='off')
    
    return JsonResponse({'success': True})

    