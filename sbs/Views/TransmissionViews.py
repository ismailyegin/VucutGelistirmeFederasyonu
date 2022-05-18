import json
import time
from datetime import datetime

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render

from sbs.models import SportFacility
from sbs.models.ekabis.City import City
from sbs.models.ekabis.Country import Country
from sbs.models.ekabis.Communication import Communication
from sbs.models.ekabis.District import District
from sbs.models.tvfbf.Club import Club


@login_required
def getLimitOffset(request):
    try:
        with transaction.atomic():
            current_limit = Club.objects.all().count()
            if request.method == 'POST':
                limit = request.POST['limit']
                offset = request.POST['offset']
                x = TransmissionClub(request, limit, offset)
                if x:
                    messages.success(request, 'Kulüpler Başarıyla Kayıt Edilmiştir.')
                else:
                    messages.warning(request, 'Kulüp aktarma işlemi yapılamadı.')
                return redirect('sbs:getLimitOffset')

            return render(request, 'TVGFBF/Club/transmissionClub.html', {'current_limit': current_limit})
    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('sbs:return_clubs')


def TransmissionClub(request, limit, offset):
    try:
        with transaction.atomic():

            url = 'https://servis3.gsb.gov.tr/SporFedProtokol/api/FederasyonServisleri/KulupleriGetir?limit=' + limit + '&offset=' + offset + ''

            payload = {}
            files = {}
            headers = {
                'Authorization': 'Basic dnVjdXRnZWxpc3Rpcm1lYWt0YXJpbTphMzE5YzczNC03ZjhlLTQ4NzQtYmExYy00YzU4MmU2NjExYTg='
            }

            response = requests.request("GET", url, headers=headers, data=payload, files=files)

            x = json.loads(response.text)

            if x['Data']:
                for club in x['Data']:
                    id = club['DerbisKutukNo']
                    if id:
                        url = 'https://servis3.gsb.gov.tr/SporFedProtokol/api/FederasyonServisleri/KulupGetirDetayli?kulupGuid=00000000-0000-0000-0000-000000000000&derbisKutukNo=' + id + ''

                        payload = {}
                        files = {}
                        headers = {
                            'Authorization': 'Basic dnVjdXRnZWxpc3Rpcm1lYWt0YXJpbTphMzE5YzczNC03ZjhlLTQ4NzQtYmExYy00YzU4MmU2NjExYTg='
                        }

                        response = requests.request("GET", url, headers=headers, data=payload, files=files)
                        y = json.loads(response.text)
                        if y['Data']:
                            clup_info = y['Data'][0]
                            country = 'TÜRKİYE CUMHURİYETİ'
                            if Club.objects.filter(guidId=club['KulupGuid']):
                                sport_club = Club.objects.get(guidId=club['KulupGuid'])
                                sport_club.isMatch = True
                                sport_club.name = clup_info['KulupAdi']
                                sport_club.guidId = clup_info['KulupGuid']

                                foundingDate = datetime.strptime(clup_info['KurulusTarihi'].split('T')[0],
                                                                 '%Y-%m-%d')
                                sport_club.foundingDate = datetime.strptime(str(foundingDate.date()),
                                                                            '%Y-%m-%d').strftime(
                                    "%d/%m/%Y")
                                communication = Communication.objects.filter(
                                    city=City.objects.get(pk=int(clup_info['IlId'])),
                                    phoneNumber=clup_info['Telefon'],
                                    address=clup_info['Adres'],
                                    town=clup_info['IlceAdi'], country=Country.objects.get(name=country))
                                if communication:

                                    communication = Communication.objects.get(
                                        city=City.objects.get(pk=int(clup_info['IlId'])),
                                        phoneNumber=clup_info['Telefon'], country=Country.objects.get(name=country),
                                        address=clup_info['Adres'], town=clup_info['IlceAdi'])
                                else:
                                    communication = Communication(
                                        city=City.objects.get(pk=int(clup_info['IlId'])),
                                        phoneNumber=clup_info['Telefon'], country=Country.objects.get(name=country),
                                        address=clup_info['Adres'], town=clup_info['IlceAdi'])
                                    communication.save()
                                sport_club.communication = communication
                                # sport_club.foundingDate = datetime.strptime(clup_info['KurulusTarihi'].replace('.', '-'),
                                #                                             '%d-%m-%Y')
                                sport_club.derbis = clup_info['DerbisKutukNo']
                                sport_club.save()
                            else:
                                new_club = Club()
                                communication = Communication(city=City.objects.get(pk=int(clup_info['IlId'])),
                                                              phoneNumber=clup_info['Telefon'],
                                                              address=clup_info['Adres'],
                                                              town=clup_info['IlceAdi'],
                                                              country=Country.objects.get(name=country))
                                communication.save()
                                new_club.name = clup_info['KulupAdi']
                                new_club.communication = communication
                                foundingDate = datetime.strptime(clup_info['KurulusTarihi'].split('T')[0],
                                                                 '%Y-%m-%d')
                                new_club.foundingDate = datetime.strptime(str(foundingDate.date()),
                                                                          '%Y-%m-%d').strftime("%d/%m/%Y")
                                new_club.derbis = clup_info['DerbisKutukNo']
                                new_club.guidId = clup_info['KulupGuid']

                                new_club.save()
                                time.sleep(2)
                return True


    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('sbs:return_clubs')


def TransmissionClubDetail(request, derbisKutukNo):
    try:
        with transaction.atomic():
            id = derbisKutukNo
            url = 'https://servis3.gsb.gov.tr/SporFedProtokol/api/FederasyonServisleri/KulupGetirDetayli?derbisKutukNo=' + id + '&KulupGuid=00000000-0000-0000-0000-000000000000'

            payload = {}
            files = {}
            headers = {
                'Authorization': 'Basic dnVjdXRnZWxpc3Rpcm1lYWt0YXJpbTphMzE5YzczNC03ZjhlLTQ4NzQtYmExYy00YzU4MmU2NjExYTg='
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


def GetCurrentFacilityDetail(request):
    try:
        with transaction.atomic():
            if request.method == 'POST':
                name = request.POST['name']
                club_info = SportFacility.objects.get(name__icontains=name)

                info = {}
                info['name'] = club_info.name
                info['derbis'] = club_info.derbis

                info['mersis'] = club_info.mersis
                info['permitDate'] = club_info.permitDate
                info['coordinate'] = club_info.coordinate
                info['status'] = club_info.status

                registrationNumber = 'yok'
                if club_info.registrationNumber:
                    registrationNumber = club_info.registrationNumber
                info['registrationNumber'] = registrationNumber
                taxNumber = 'yok'
                if club_info.taxNumber:
                    taxNumber = club_info.taxNumber
                info['taxNumber'] = taxNumber

                return JsonResponse({'status': 'Success',
                                     'result': info,
                                     })

    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('sbs:return_clubs')


def GetCurrentClubDetail(request):
    try:
        with transaction.atomic():
            id = request.POST['derbis']
            club_info = Club.objects.get(derbis=id)

            club = {}
            club['KulupAdi'] = club_info.name
            club['KurulusTarihi'] = club_info.foundingDate
            city_name = ''
            if club_info.communication.city:
                city_name = club_info.communication.city.name
            club['Il'] = city_name
            club['Telefon'] = club_info.communication.phoneNumber
            club['Adres'] = club_info.communication.address
            club['Ilce'] = club_info.communication.town
            club['DerbisKutukNo'] = club_info.derbis
            club['Eposta'] = club_info.clubMail
            club['Faks'] = club_info.communication.fax
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
                    return JsonResponse({'status': 'Fail', 'msg': 'Bu derbis numarasına ait bir kulüp bulunamadı.',
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


def TransmissionCity(request):
    try:
        with transaction.atomic():
            url = 'https://servis3.gsb.gov.tr/SporFedProtokol/api/FederasyonServisleri/IlListesiGetir'

            payload = {}
            files = {}
            headers = {
                'Authorization': 'Basic dnVjdXRnZWxpc3Rpcm1lYWt0YXJpbTphMzE5YzczNC03ZjhlLTQ4NzQtYmExYy00YzU4MmU2NjExYTg='
            }

            response = requests.request("GET", url, headers=headers, data=payload, files=files)
            y = json.loads(response.text)
            if y['Data']:
                for club_info in y['Data']:
                    if not City.objects.filter(plateNo=club_info['IlId']):
                        city = City()
                        city.name = club_info['IlAdi']
                        city.plateNo = club_info['IlId']
                        city.save()

            messages.success(request, 'İl aktarma işlemi yapıldı.')
            return redirect('sbs:view_admin')


    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('sbs:view_admin')


def TransmissionCountry(request):
    try:
        with transaction.atomic():
            url = 'https://servis3.gsb.gov.tr/SporFedProtokol/api/FederasyonServisleri/UlkeListesiGetir'

            payload = {}
            files = {}
            headers = {
                'Authorization': 'Basic dnVjdXRnZWxpc3Rpcm1lYWt0YXJpbTphMzE5YzczNC03ZjhlLTQ4NzQtYmExYy00YzU4MmU2NjExYTg='
            }

            response = requests.request("GET", url, headers=headers, data=payload, files=files)
            y = json.loads(response.text)
            if y:
                for club_info in y:
                    if not Country.objects.filter(name=club_info['UlkeAdi']):
                        country = Country()
                        country.name = club_info['UlkeAdi']
                        country.save()

            messages.success(request, 'Ülke aktarma işlemi yapıldı.')
            return redirect('sbs:view_admin')


    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('sbs:view_admin')


def TransmissionDistrict(request):
    try:
        with transaction.atomic():
            for city in City.objects.all():
                url = 'https://servis3.gsb.gov.tr/SporFedProtokol/api/FederasyonServisleri/IlceListesiGetir?ilId=' + str(
                    city.pk) + ''

                payload = {}
                files = {}
                headers = {
                    'Authorization': 'Basic dnVjdXRnZWxpc3Rpcm1lYWt0YXJpbTphMzE5YzczNC03ZjhlLTQ4NzQtYmExYy00YzU4MmU2NjExYTg='
                }

                response = requests.request("GET", url, headers=headers, data=payload, files=files)
                y = json.loads(response.text)
                if y['Data']:
                    for club_info in y['Data']:
                        if not District.objects.filter(name=club_info['IlceAdi']).filter(city=city):
                            district = District()
                            district.name = club_info['IlceAdi']
                            district.city = city
                            district.save()

            messages.success(request, 'İlçe aktarma işlemi yapıldı.')
            return redirect('sbs:view_admin')


    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('sbs:view_admin')


def DeleteClub(request):
    try:
        with transaction.atomic():
            for club in Club.objects.all():
                club.delete()
                time.sleep(2)

            messages.success(request, 'işlem yapıldı.')
            return redirect('sbs:view_admin')


    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('sbs:view_admin')
