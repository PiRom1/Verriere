from datetime import timedelta
from django.http import HttpResponse
from django.utils import timezone
from controller.models import Ventilateur, Capteur, Releve, CapteurMesure, VentilateurEtat
from django.shortcuts import render
from controller.controls.ventilateur_controls import get_etat_ventilateur
from constance import config



def index(request):
    """
    Page d'accueil : présente ma verrière et mes modules
    """

    ventilateurs = Ventilateur.objects.all()
    capteurs = Capteur.objects.all()

    # Historique des dernières heures (réglage DELAIS_RELEVES_INDEX), dans l'ordre chronologique,
    # mesures chargées en une requête.
    depuis = timezone.now() - timedelta(hours=config.DELAIS_RELEVES_INDEX)
    releves_historique = list(Releve.objects.filter(datetime__gte=depuis).order_by('datetime'))
    mesures = {(m.releve_id, m.capteur_id): m
               for m in CapteurMesure.objects.filter(releve__in=releves_historique)}

    capteurs_data = []
    historique_capteurs = []

    for capteur in capteurs:
        derniere_mesure = capteur.mesures.order_by('-releve__datetime').first()
        capteurs_data.append({'capteur' : capteur.to_dict(),
                              'temperature' : derniere_mesure.temperature if derniere_mesure else None,
                              'humidite' : derniere_mesure.humidite if derniere_mesure else None})

        # None quand un relevé n'a pas de mesure pour ce capteur (trou dans la courbe).
        historique_capteurs.append({'nom' : str(capteur),
                                    'etage' : capteur.etage,
                                    'temperature' : [getattr(mesures.get((r.id, capteur.id)), 'temperature', None) for r in releves_historique],
                                    'humidite' : [getattr(mesures.get((r.id, capteur.id)), 'humidite', None) for r in releves_historique]})

    # États des ventilateurs à chaque relevé (une requête). None = pas d'état enregistré.
    etats = {(e.releve_id, e.ventilateur_id): e.est_allume
             for e in VentilateurEtat.objects.filter(releve__in=releves_historique)}
    historique_ventilateurs = [{'nom' : str(v),
                                'etage' : v.etage,
                                'etats' : [etats.get((r.id, v.id)) for r in releves_historique]}
                               for v in ventilateurs.order_by('etage')]

    historique = {
        'ids' : [r.id for r in releves_historique],
        'dates' : [timezone.localtime(r.datetime).strftime('%d/%m %H:%M') for r in releves_historique],
        'capteurs' : historique_capteurs,
        'ventilateurs' : historique_ventilateurs,
    }


    # KPIs sur l'historique affiché (tous capteurs confondus, les trous None sont ignorés)
    kpis = None
    temperatures = [t for c in historique_capteurs for t in c['temperature'] if t is not None]
    humidites = [h for c in historique_capteurs for h in c['humidite'] if h is not None]
    
    if releves_historique and temperatures and humidites:
        kpis = {'dernier_releve' : releves_historique[-1].datetime,
                'nb_releves' : len(releves_historique),
                'temperature' : {'min' : min(temperatures), 'moyenne' : sum(temperatures) / len(temperatures), 'max' : max(temperatures)},
                'humidite' : {'min' : min(humidites), 'moyenne' : sum(humidites) / len(humidites), 'max' : max(humidites)}}

    context = {
        'ventilateurs' : [{'ventilateur' : ventilateur.to_dict(), 'etat' : get_etat_ventilateur(ventilateur)} for ventilateur in ventilateurs],
        'capteurs' : capteurs_data,
        'historique' : historique,
        'heures_historique' : config.DELAIS_RELEVES_INDEX,
        'kpis' : kpis
    }
    
    return render(request, 'controller/app/index.html', context)




def home(request):
    return HttpResponse("Home page")