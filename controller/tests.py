from django.test import TestCase, override_settings

from controller.controls.ventilateur_controls import commander_ventilateur
from controller.models import Ventilateur


class HardwareFakeTests(TestCase):
    def test_mode_fake_par_defaut_sur_pc(self):
        from django.conf import settings
        self.assertEqual(settings.HARDWARE_MODE, "fake")

    def test_commander_ventilateur_allume_puis_eteint(self):
        from hardware import relais

        ventilateur = Ventilateur.objects.create(nom="Haut", nb_ventilateurs=2, etage=1, gpio_broche=17)

        commander_ventilateur(ventilateur, "on")
        ventilateur.refresh_from_db()
        self.assertTrue(ventilateur.est_allume)
        self.assertEqual(relais(17).value, 1)

        commander_ventilateur(ventilateur, "off")
        ventilateur.refresh_from_db()
        self.assertFalse(ventilateur.est_allume)
        self.assertEqual(relais(17).value, 0)

    def test_dht_fake_renvoie_des_valeurs_plausibles(self):
        from hardware import dht

        capteur = dht(4)
        self.assertTrue(18.0 <= capteur.temperature <= 30.0)
        self.assertTrue(40.0 <= capteur.humidity <= 80.0)
        capteur.exit()  # ne doit pas lever
