from django.contrib import admin

from controller.models import Capteur, CapteurMesure, Releve, Ventilateur, VentilateurEtat


@admin.register(Ventilateur)
class VentilateurAdmin(admin.ModelAdmin):
    list_display = ("nom", "etage", "nb_ventilateurs", "gpio_broche")
    list_filter = ("etage",)
    search_fields = ("nom",)
    ordering = ("etage", "nom")


@admin.register(Capteur)
class CapteurAdmin(admin.ModelAdmin):
    list_display = ("nom", "etage", "gpio_broche")
    list_filter = ("etage",)
    search_fields = ("nom",)
    ordering = ("etage", "nom")


class CapteurMesureInline(admin.TabularInline):
    model = CapteurMesure
    extra = 0


class VentilateurEtatInline(admin.TabularInline):
    model = VentilateurEtat
    extra = 0


@admin.register(Releve)
class ReleveAdmin(admin.ModelAdmin):
    list_display = ("datetime",)
    date_hierarchy = "datetime"
    ordering = ("-datetime",)
    readonly_fields = ("datetime",)
    inlines = (CapteurMesureInline, VentilateurEtatInline)


@admin.register(CapteurMesure)
class CapteurMesureAdmin(admin.ModelAdmin):
    list_display = ("releve", "capteur", "temperature", "humidite")
    list_filter = ("capteur",)
    ordering = ("-releve__datetime",)


@admin.register(VentilateurEtat)
class VentilateurEtatAdmin(admin.ModelAdmin):
    list_display = ("releve", "ventilateur", "est_allume")
    list_filter = ("ventilateur", "est_allume")
    ordering = ("-releve__datetime",)
