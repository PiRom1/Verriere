"""
Génère des relevés fictifs (température, humidité, état des ventilateurs)
sur les N derniers jours, pour tester l'interface sans attendre.

Usage : python manage.py generer_releves_fictifs [--jours 2] [--periode 10]
"""

import math
import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from controller.models import Capteur, CapteurMesure, Releve, Ventilateur, VentilateurEtat


class Command(BaseCommand):
    help = "Génère des relevés fictifs sur les N derniers jours"

    def add_arguments(self, parser):
        parser.add_argument("--jours", type=int, default=2, help="Nombre de jours à couvrir (défaut : 2)")
        parser.add_argument("--periode", type=int, default=10, help="Minutes entre deux relevés (défaut : 10)")

    @transaction.atomic
    def handle(self, *args, **options):
        capteurs = list(Capteur.objects.all())
        ventilateurs = list(Ventilateur.objects.all())
        if not capteurs:
            self.stderr.write("Aucun capteur en base : rien à générer.")
            return

        fin = timezone.now()
        debut = fin - timedelta(days=options["jours"])
        periode = timedelta(minutes=options["periode"])

        nb = 0
        instant = debut
        while instant <= fin:
            releve = Releve.objects.create()
            # datetime est en auto_now_add : on le force après coup.
            Releve.objects.filter(pk=releve.pk).update(datetime=instant)

            heure = instant.astimezone(timezone.get_current_timezone())
            heure_decimale = heure.hour + heure.minute / 60
            # Cycle journalier : minimum vers 5h, maximum vers 17h.
            cycle = math.sin((heure_decimale - 11) / 24 * 2 * math.pi)

            temperature_ambiante = 19 + 7 * cycle
            for capteur in capteurs:
                temperature = round(temperature_ambiante + capteur.etage * 0.8 + random.gauss(0, 0.4), 1)
                humidite = round(max(30, min(95, 80 - 1.8 * (temperature - 15) + random.gauss(0, 3))), 1)
                CapteurMesure.objects.create(releve=releve, capteur=capteur, temperature=temperature, humidite=humidite)

            for ventilateur in ventilateurs:
                VentilateurEtat.objects.create(releve=releve, ventilateur=ventilateur, est_allume=temperature_ambiante > 23)

            nb += 1
            instant += periode

        self.stdout.write(self.style.SUCCESS(
            f"{nb} relevés générés du {debut:%d/%m %H:%M} au {fin:%d/%m %H:%M} "
            f"({len(capteurs)} capteur(s), {len(ventilateurs)} ventilateur(s))"
        ))
