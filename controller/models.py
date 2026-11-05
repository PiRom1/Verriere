from django.db import models



## Matériel

class Ventilateur(models.Model):
    """
    Un groupe de ventilateurs
    """

    nom = models.CharField(max_length=100)
    nb_ventilateurs = models.IntegerField()
    etage = models.IntegerField()
    gpio_broche = models.PositiveSmallIntegerField(unique=True, help_text="Numéro BCM de la broche DATA")

    def __str__(self):
        return f"{self.nom} (étage {self.etage})"


class Capteur(models.Model):
    """
    Un capteur de température et humidité
    """

    nom = models.CharField(max_length=100)
    etage = models.IntegerField()
    gpio_broche = models.PositiveSmallIntegerField(unique=True, help_text="Numéro BCM de la broche DATA")

    def __str__(self):
        return f"{self.nom} (étage {self.etage})"



## Mesures


class Releve(models.Model):
    """
    Un relevé à un instant précis (capteurs, état des ventilateurs, ... )
    """

    datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    erreurs = models.JSONField(null=True, blank=True, default=None)


class CapteurMesure(models.Model):
    """
    Une mesure des capteurs
    """

    releve = models.ForeignKey(Releve, on_delete=models.CASCADE, related_name="mesures")
    capteur = models.ForeignKey(Capteur, on_delete=models.CASCADE, related_name="mesures")
    temperature = models.FloatField()
    humidite = models.FloatField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["releve", "capteur"], name="une_mesure_par_capteur_par_releve")]

class VentilateurEtat(models.Model):
    """
    Un état de ventilateur
    """

    releve = models.ForeignKey(Releve, on_delete=models.CASCADE, related_name="etats_ventilateurs")
    ventilateur = models.ForeignKey(Ventilateur, on_delete=models.CASCADE, related_name="etats")
    est_allume = models.BooleanField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["releve", "ventilateur"], name="une_mesure_par_ventilateur_par_releve")]

