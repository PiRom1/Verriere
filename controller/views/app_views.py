from django.http import HttpResponse
from django.utils import timezone
from controller.models import Ventilateur, Capteur, Releve, CapteurMesure
from django.shortcuts import render
from controller.controls.ventilateur_controls import get_etat_ventilateur

NB_RELEVES_HISTORIQUE = 288  # 2 jours à un relevé toutes les 10 minutes


def index(request):
    """
    Page d'accueil : présente ma verrière et mes modules
    """

    ventilateurs = Ventilateur.objects.all()
    capteurs = Capteur.objects.all()
    derniers_releves = Releve.objects.all().order_by('-datetime')[:10]

    # Historique dans l'ordre chronologique, mesures chargées en une requête.
    releves_historique = list(Releve.objects.order_by('-datetime')[:NB_RELEVES_HISTORIQUE])[::-1]
    mesures = {(m.releve_id, m.capteur_id): m
               for m in CapteurMesure.objects.filter(releve__in=releves_historique)}

    capteurs_data = []
    historique_capteurs = []

    for capteur in capteurs:
        derniere_mesure = capteur.mesures.order_by('-releve__datetime').first()
        capteurs_data.append({'capteur' : capteur,
                              'temperature' : derniere_mesure.temperature if derniere_mesure else None,
                              'humidite' : derniere_mesure.humidite if derniere_mesure else None})

        # None quand un relevé n'a pas de mesure pour ce capteur (trou dans la courbe).
        historique_capteurs.append({'nom' : str(capteur),
                                    'temperature' : [getattr(mesures.get((r.id, capteur.id)), 'temperature', None) for r in releves_historique],
                                    'humidite' : [getattr(mesures.get((r.id, capteur.id)), 'humidite', None) for r in releves_historique]})

    historique = {
        'dates' : [timezone.localtime(r.datetime).strftime('%d/%m %H:%M') for r in releves_historique],
        'capteurs' : historique_capteurs,
    }

    context = {
        'ventilateurs' : [{'ventilateur' : ventilateur, 'etat' : get_etat_ventilateur(ventilateur)} for ventilateur in ventilateurs],
        'capteurs' : capteurs_data,
        'derniers_releves' : derniers_releves,
        'historique' : historique,
    }
    
    return render(request, 'controller/app/index.html', context)




def home(request):
    return HttpResponse("Home page")