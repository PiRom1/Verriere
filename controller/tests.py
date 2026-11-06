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

        # L'état n'est plus stocké sur le modèle : il est lu sur le relais.
        commander_ventilateur(ventilateur, "on")
        self.assertEqual(relais(17).value, 1)

        commander_ventilateur(ventilateur, "off")
        self.assertEqual(relais(17).value, 0)

    def test_dht_fake_renvoie_des_valeurs_plausibles(self):
        from hardware import dht

        capteur = dht(4)
        self.assertTrue(18.0 <= capteur.temperature <= 30.0)
        self.assertTrue(40.0 <= capteur.humidity <= 80.0)
        capteur.exit()  # ne doit pas lever


class CapteurVueTests(TestCase):
    """La page d'un capteur ne doit jamais faire 500, quel que soit l'état des relevés."""

    def setUp(self):
        from controller.models import Capteur
        self.capteur = Capteur.objects.create(nom="Bas", etage=0, gpio_broche=4)
        self.autre = Capteur.objects.create(nom="Haut", etage=1, gpio_broche=17)

    def test_sans_aucun_releve(self):
        reponse = self.client.get(f"/capteur/{self.capteur.id}")
        self.assertEqual(reponse.status_code, 200)
        self.assertIsNone(reponse.context["temperature"])
        self.assertIsNone(reponse.context["date_dernier_releve"])

    def test_releve_sans_mesure_pour_ce_capteur(self):
        from controller.models import Releve, CapteurMesure
        releve = Releve.objects.create()
        CapteurMesure.objects.create(releve=releve, capteur=self.autre, temperature=21, humidite=51)
        reponse = self.client.get(f"/capteur/{self.capteur.id}")
        self.assertEqual(reponse.status_code, 200)
        self.assertIsNone(reponse.context["temperature"])

    def test_affiche_la_derniere_mesure_de_ce_capteur(self):
        from controller.models import Releve, CapteurMesure
        ancien = Releve.objects.create()
        CapteurMesure.objects.create(releve=ancien, capteur=self.capteur, temperature=10, humidite=40)
        recent = Releve.objects.create()
        CapteurMesure.objects.create(releve=recent, capteur=self.autre, temperature=99, humidite=99)
        CapteurMesure.objects.create(releve=recent, capteur=self.capteur, temperature=20, humidite=50)
        reponse = self.client.get(f"/capteur/{self.capteur.id}")
        self.assertEqual(reponse.status_code, 200)
        self.assertEqual(reponse.context["temperature"], 20)
        self.assertEqual(reponse.context["humidite"], 50)
        self.assertEqual(reponse.context["date_dernier_releve"], recent.datetime)


class IndexVueTests(TestCase):
    def test_liens_ventilateurs_contiennent_l_id(self):
        from controller.models import Ventilateur
        ventilateur = Ventilateur.objects.create(nom="Haut", nb_ventilateurs=2, etage=1, gpio_broche=17)
        reponse = self.client.get("/")
        self.assertEqual(reponse.status_code, 200)
        self.assertContains(reponse, f'href="/ventilateur/{ventilateur.id}"')

    def test_index_sans_releve_avec_capteur(self):
        from controller.models import Capteur
        Capteur.objects.create(nom="Bas", etage=0, gpio_broche=4)
        reponse = self.client.get("/")
        self.assertEqual(reponse.status_code, 200)
        self.assertEqual(reponse.context["historique"]["dates"], [])

    def test_index_historique_chronologique_avec_trous(self):
        from controller.models import Capteur, Releve, CapteurMesure
        capteur = Capteur.objects.create(nom="Bas", etage=0, gpio_broche=4)
        ancien = Releve.objects.create()
        CapteurMesure.objects.create(releve=ancien, capteur=capteur, temperature=10, humidite=40)
        Releve.objects.create()  # relevé sans mesure (lecture ratée)
        reponse = self.client.get("/")
        self.assertEqual(reponse.status_code, 200)
        historique = reponse.context["historique"]
        self.assertEqual(len(historique["dates"]), 2)
        self.assertEqual(historique["capteurs"][0]["temperature"], [10, None])
        self.assertEqual(reponse.context["capteurs"][0]["temperature"], 10)
