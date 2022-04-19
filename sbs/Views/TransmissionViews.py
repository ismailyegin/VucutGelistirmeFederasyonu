import json
from datetime import datetime

import requests
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render

from sbs.models.ekabis.City import City
from sbs.models.ekabis.Country import Country
from sbs.models.ekabis.Communication import Communication
from sbs.models.tvfbf.Club import Club


def TransmissionClub(request, limit, offset):
    try:
        with transaction.atomic():

            url = 'https://servis3.gsb.gov.tr/fedprotokoltest/api/FederasyonServisleri/KulupleriGetir?limit=' + limit + '&offset=' + offset + ''

            payload = {}
            files = {}
            headers = {
                'Authorization': 'Basic YmFkbWludG9uYWt0YXJpbToxMjM0NQ=='
            }

            response = requests.request("GET", url, headers=headers, data=payload, files=files)

            x = json.loads(response.text)

            if x['Data']:
                for club in x['Data']:
                    id = club['DerbisKutukNo']
                    url = 'https://servis3.gsb.gov.tr/SporFedProtokol/api/FederasyonServisleri/KulupGetirDetayli?derbisKutukNo=' + id + '&KulupGuid=00000000-0000-0000-0000-000000000000'

                    payload = {}
                    files = {}
                    headers = {
                        'Authorization': 'Basic YmFkbWludG9uYWt0YXJpbTo4NTgzYTg1Zi1mYTU5LTRiMzUtYmQ1OC1mYTJlYzg1YmRhMDk='
                    }

                    response = requests.request("GET", url, headers=headers, data=payload, files=files)
                    y = json.loads(response.text)
                    if y['Data']:
                        clup_info = y['Data'][0]
                        if Club.objects.filter(name__icontains=club['KulupAdi']):
                            sport_club = Club.objects.get(name__icontains=club['KulupAdi'])
                            sport_club.isMatch = True
                            sport_club.name = clup_info['KulupAdi']
                            foundingDate = datetime.strptime(clup_info['KurulusTarihi'].split('T')[0],
                                                             '%Y-%m-%d')
                            sport_club.foundingDate = datetime.strptime(str(foundingDate.date()), '%Y-%m-%d').strftime(
                                "%d/%m/%Y")
                            communication = Communication.objects.filter(
                                city=City.objects.get(pk=int(clup_info['IlId'])),
                                phoneNumber=clup_info['Telefon'],
                                address=clup_info['Adres'],
                                town=clup_info['IlceAdi'], country=Country.objects.get(name='TÜRKİYE'))
                            if communication:
                                communication = Communication.objects.get(
                                    city=City.objects.get(pk=int(clup_info['IlId'])),
                                    phoneNumber=clup_info['Telefon'], country=Country.objects.get(name='TÜRKİYE'),
                                    address=clup_info['Adres'], town=clup_info['IlceAdi'])
                            else:
                                communication = Communication(
                                    city=City.objects.get(pk=int(clup_info['IlId'])),
                                    phoneNumber=clup_info['Telefon'], country=Country.objects.get(name='TÜRKİYE'),
                                    address=clup_info['Adres'], town=clup_info['IlceAdi'])
                                communication.save()
                            sport_club.communication = communication
                            # sport_club.foundingDate = datetime.strptime(clup_info['KurulusTarihi'].replace('.', '-'),
                            #                                             '%d-%m-%Y')
                            sport_club.derbisKutukNo = clup_info['DerbisKutukNo']
                            sport_club.save()
                        else:
                            new_club = Club()
                            communication = Communication(city=City.objects.get(pk=int(clup_info['IlId'])),
                                                          phoneNumber=clup_info['Telefon'],
                                                          address=clup_info['Adres'],
                                                          town=clup_info['IlceAdi'],
                                                          country=Country.objects.get(name='TÜRKİYE'))
                            communication.save()
                            new_club.name = clup_info['KulupAdi']
                            new_club.communication = communication
                            foundingDate = datetime.strptime(clup_info['KurulusTarihi'].split('T')[0],
                                                             '%Y-%m-%d')
                            new_club.foundingDate = datetime.strptime(str(foundingDate.date()),
                                                                      '%Y-%m-%d').strftime("%d/%m/%Y")
                            new_club.derbisKutukNo = clup_info['DerbisKutukNo']
                            new_club.save()

                messages.success(request, 'Kulüp Başarıyla Kayıt Edilmiştir.')


    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('sbs:kulupler')


def TransmissionClubDetail(request, derbisKutukNo):
    try:
        with transaction.atomic():
            id = derbisKutukNo
            url = 'https://servis3.gsb.gov.tr/SporFedProtokol/api/FederasyonServisleri/KulupGetirDetayli?derbisKutukNo=' + id + '&KulupGuid=00000000-0000-0000-0000-000000000000'

            payload = {}
            files = {}
            headers = {
                'Authorization': 'Basic YmFkbWludG9uYWt0YXJpbTo4NTgzYTg1Zi1mYTU5LTRiMzUtYmQ1OC1mYTJlYzg1YmRhMDk='
            }

            response = requests.request("GET", url, headers=headers, data=payload, files=files)
            y = json.loads(response.text)
            result = []
            if y['Data']:
                club_info = y['Data'][0]
                club = {}
                club['KulupAdi'] = club_info['KulupAdi']
                club['KurulusTarihi'] = datetime.strptime(club_info['KurulusTarihi'].split('T')[0],
                                                          '%Y-%m-%d').date()
                club['Il'] = City.objects.get(pk=int(club_info['IlId'])).name
                club['Telefon'] = club_info['Telefon']
                club['Adres'] = club_info['Adres']
                club['Ilce'] = club_info['IlceAdi']
                club['DerbisKutukNo'] = club_info['DerbisKutukNo']
                club['Eposta'] = club_info['Eposta']
                club['KulupNo'] = club_info['KulupNoFormatli']
                club['Faks'] = club_info['Faks']
                club['Guid'] = id
                club['FaaliyetDurumu'] = club_info['FaaliyetDurumu']
                result.append(club)
            return result


    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('sbs:return_clubs')


def GetCurrentClubDetail(request):
    try:
        with transaction.atomic():
            id = request.POST['derbis']
            club_info=Club.objects.get(derbis=id)

            club = {}
            club['KulupAdi'] = club_info.name
            club['KurulusTarihi'] = club_info.foundingDate
            city_name=''
            if club_info.communication.city:
                city_name=club_info.communication.city.name
            club['Il'] = city_name
            club['Telefon'] = club_info.communication.phoneNumber
            club['Adres'] =club_info.communication.address
            club['Ilce'] = club_info.communication.town
            club['DerbisKutukNo'] = club_info.derbis
            club['Eposta'] = club_info.clubMail
            club['Faks'] =  club_info.communication.fax
            club['Guid'] = club_info.guidId


            return JsonResponse({'status': 'Success',
                                     'result': club,
                                     })

    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('sbs:return_clubs')


def transmissionOffsetLimit(request):
    try:
        with transaction.atomic():
            if request.method == 'POST':
                # offset = str(request.POST['offset'])
                # limit = str(request.POST['limit'])
                guid = str(request.POST['guid'])
                result = TransmissionClubDetail(request, guid)
                if result:
                    return JsonResponse({'status': 'Success',
                                         'result': result,
                                         })
                else:
                    return JsonResponse({'status': 'Fail', 'msg': 'Kulüp Bulunamadı',
                                         'result': result,
                                         })
    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('sbs:return_clubs')


def getClubForRegisterManager(request):
    try:
        with transaction.atomic():

            if request.method == 'POST':
                guid = str(request.POST['guid'])
                result = []
                if Club.objects.filter(guidId=guid):
                    club = Club.objects.get(guidId=guid)
                    clubList = {}
                    clubList['KulupAdi'] = club.name
                    if club.foundingDate:
                        clubList['KurulusTarihi'] = club.foundingDate
                    else:
                        clubList['KurulusTarihi'] = ''
                    clubList['Il'] = club.communication.city.name
                    clubList['Telefon'] = club.communication.phoneNumber
                    clubList['Adres'] = club.communication.address
                    clubList['Ilce'] = club.communication.town
                    clubList['DerbisKutukNo'] = club.derbis
                    clubList['Eposta'] = club.clubMail
                    clubList['Faks'] = club.communication.fax
                    clubList['Guid'] = club.guidId
                    clubList['FaaliyetDurumu'] = club.infoStatus
                    result.append(clubList)
                if result:
                    return JsonResponse({'status': 'Success',
                                         'result': result,
                                         })
                else:
                    return JsonResponse({'status': 'Fail', 'msg': 'Kulüp Bulunamadı',
                                         'result': result,
                                         })
    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('sbs:return_clubs')

# from apscheduler.schedulers.background import BackgroundScheduler
#
#
# def test():
#     print('test')
#
# def test2():
#     print('test2')
#
#
# scheduler = BackgroundScheduler(timezone="Europe/Istanbul")
# scheduler.add_job(test, 'cron', year='2022', month='1,3,5', day='21,22', hour='10,11', minute='8')
# scheduler.add_job(test2, 'cron', year='*', month='*', day='*', hour='*', minute='41,45')
# scheduler.start()
