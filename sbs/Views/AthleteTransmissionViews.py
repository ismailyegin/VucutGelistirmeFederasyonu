import json
from datetime import datetime

import requests
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect

from sbs.models.ekabis.City import City


def transmissionAthleteTc(request):
    try:
        with transaction.atomic():
            if request.method == 'POST':
                tc = str(request.POST['tc'])
                result = TransmissionAthleteDetail(request, tc)
                if result:
                    return JsonResponse({'status': 'Success',
                                         'result': result,
                                         })
                else:
                    return JsonResponse({'status': 'Fail', 'msg': 'Bu Tc kimlik  numarasına ait bir sporcu bulunamadı.',
                                         'result': result,
                                         })
    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('accounts:pre_registration_athelete')


def TransmissionAthleteDetail(request, tc):
    try:
        with transaction.atomic():
            id = tc
            url = 'https://servis3.gsb.gov.tr/SporFedProtokol/api/FederasyonServisleri/SporcuGetir?tc=' + id + ''

            payload = {}
            files = {}
            headers = {
                'Authorization': 'Basic dnVjdXRnZWxpc3Rpcm1lYWt0YXJpbTphMzE5YzczNC03ZjhlLTQ4NzQtYmExYy00YzU4MmU2NjExYTg='
            }

            response = requests.request("GET", url, headers=headers, data=payload, files=files)
            y = json.loads(response.text)
            result = []
            if y['Data']:
              return  y['Data'][0]


    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('sbs:return_clubs')
