from django.http import HttpResponse
from controller.models import Ventilateur, Capteur, Releve
from django.shortcuts import render


def index(request):
    """
    Page d'accueil : présente ma verrière et mes modules
    """

    ventilateurs = Ventilateur.objects.all()
    capteurs = Capteur.objects.all()
    derniers_releves = Releve.objects.all().order_by('datetime')[:10]

    context = {
        'ventilateurs' : ventilateurs,
        'capteurs' : capteurs,
        'derniers_releves' : derniers_releves
    }
    
    return render(request, 'controller/app/index.html', context)




def home(request):
    return HttpResponse("Home page")