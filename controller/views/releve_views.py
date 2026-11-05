"""
Écriture des relevés
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from controller.controls.releve_controls import ecrire_releve
import json
from django.conf import settings


@csrf_exempt
@require_POST
def ecrire_releve_view(request):
    """
    Déclenche l'écriture d'un relevé. Appelé par le cron (curl) ou par l'interface.
    """

    try:
        payload = json.loads(request.body)
    except Exception as e:
        return JsonResponse({'success' : False, 'error' : "Donne au moins un body frérot ... "})

    if 'code_secret' in payload:

        if payload['code_secret'] == settings.CODE_SECRET_RELEVE:
            ecrire_releve()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error' : "T'as pas le bon code secret frérot ..."})
    else:
        return JsonResponse({'success': False, "error" : "Il s'agirait de donner un code secret frérot ..."})
