from django.urls import path

from controller.views import app_views, capteur_views, ventilateur_views, releve_views

urlpatterns = [
    path("", app_views.index, name="index"),
    path("home", app_views.home, name="home"),
    path("capteur/<int:id>", capteur_views.capteur, name="capteur"),
    path("ventilateur/<int:id>", ventilateur_views.ventilateur, name="ventilateur"),

    ## Fetch URLs

    # Capteurs
    path("capteur/get_temperature_humidite", capteur_views.get_capteur_temperature_humidite, name="get_capteur_temperature_humidite"),

    # Ventilateurs
    path("ventilateur/allumer", ventilateur_views.allumer_ventilateur, name="allumer_ventilateur"),
    path("ventilateur/eteindre", ventilateur_views.eteindre_ventilateur, name="eteindre_ventilateur"),

    # Relevé
    path("releve/ecrire", releve_views.ecrire_releve_view, name="ecrire_releve"),

    
]