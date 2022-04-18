import json

import requests
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect

from sbs.models import Communication, City, Club


def ClubTransmission(request):
    try:
        with transaction.atomic():

            url = 'https://servis3.gsb.gov.tr/fedprotokoltest/api/FederasyonServisleri/KulupleriGetir?limit=1000&offset=3000'

            payload = {}
            files = {}
            headers = {
                'Authorization': 'Basic YmFkbWludG9uYWt0YXJpbTo4NTgzYTg1Zi1mYTU5LTRiMzUtYmQ1OC1mYTJlYzg1YmRhMDk='
            }

            response = requests.request("GET", url, headers=headers, data=payload, files=files)

            x = json.loads(response.text)
            addCount = 0
            updateCount = 0
            count = 0
            if x['Data']:
                for club in x['Data']:

                    if club['KulupGuid'] == None or club['KulupGuid'] == '':
                        print(club['KulupGuid'])

                    elif not Club.objects.filter(guidId=club['KulupGuid']):
                        addCount += 1
                        kulupAdi = club['KulupAdi']
                        derbisKutukNo = club['DerbisKutukNo']
                        ilAdi = club['IlAdi']
                        ilceAdi = club['IlceAdi']
                        faaliyetDurumu = club['FaaliyetDurumu']
                        adres = club['Adres']
                        telefon = club['Telefon']
                        eposta = club['Eposta']
                        websitesi = club['WebSitesi']
                        faks = club['Faks']
                        guid = club['KulupGuid']

                        clubCommunication = Communication()
                        clubCommunication.phoneNumber = telefon
                        clubCommunication.address = adres
                        clubCommunication.fax = faks
                        if City.objects.filter(name=ilAdi):
                            clubCommunication.city = City.objects.get(name=ilAdi)
                        clubCommunication.town = ilceAdi
                        clubCommunication.webSite = websitesi
                        clubCommunication.save()

                        clubSave = Club()
                        clubSave.name = kulupAdi
                        clubSave.clubMail = eposta
                        clubSave.derbis = derbisKutukNo
                        if faaliyetDurumu == 'FAAL':
                            clubSave.infoStatus = 1
                        else:
                            clubSave.infoStatus = 0
                        clubSave.username = eposta
                        clubSave.guidId = guid
                        clubSave.save()

                        clubSave.communication = clubCommunication
                        clubSave.save()
                    elif Club.objects.filter(guidId=club['KulupGuid']):
                        updateCount += 1
                        old_club = Club.objects.get(guidId=club['KulupGuid'])
                        kulupAdi = club['KulupAdi']
                        ilAdi = club['IlId']
                        ilceAdi = club['IlceAdi']
                        faaliyetDurumu = club['FaaliyetDurumu']
                        adres = club['Adres']
                        telefon = club['Telefon']
                        eposta = club['Eposta']
                        websitesi = club['WebSitesi']
                        faks = club['Faks']
                        derbisKutukNo = club['DerbisKutukNo']

                        old_club.derbis = derbisKutukNo
                        old_club.name = kulupAdi
                        old_club.clubMail = eposta
                        if faaliyetDurumu == 'FAAL':
                            old_club.infoStatus = 1
                        else:
                            old_club.infoStatus = 0

                        old_club.save()

                        com = old_club.communication
                        if ilAdi:
                            com.city = City.objects.get(pk=ilAdi)
                        com.town = ilceAdi
                        com.address = adres
                        com.phoneNumber = telefon
                        com.webSite = websitesi
                        com.fax = faks
                        com.save()




            messages.success(request, str(updateCount) + ' Kulüp Güncellendi ve ' + str(
                addCount) + ' Kulüp Başarıyla Kayıt Edilmiştir.')

            return redirect('sbs:return_clubs')


    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('sbs:return_clubs')
