import datetime
import json
import time
import traceback

import requests
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response

from sbs.models import Permission, Coach, Referee, SportFacility, ReferenceCoach, HavaLevel, EnumFields, Branch
from sbs.models.ekabis.Logs import Logs
from sbs.models.tvfbf.Club import Club
from sbs.models.tvfbf.LogAPIObject import LogAPIObject
from sbs.models.tvfbf.ReferenceReferee import ReferenceReferee
from sbs.models.tvfbf.VisaSeminar import VisaSeminar
from sbs.serializers.ClubSerializer import ClubResponseSerializer
from sbs.serializers.CoachSerializers import CoachResponseSerializer
from sbs.serializers.LogSerializers import LogResponseSerializer
from sbs.serializers.PermissionSerializers import PermissionResponseSerializer
from sbs.serializers.RefereeSerializers import RefereeResponseSerializer
from sbs.serializers.ReferenceCoachSerializers import ReferenceCoachResponseSerializer
from sbs.serializers.ReferenceRefereeSerializers import ReferenceRefereeResponseSerializer
from sbs.serializers.SportFacilitySerializers import SportFacilityResponseSerializer
from sbs.serializers.UserSerializers import UserResponseSerializer
from sbs.services import general_methods
from sbs.services.services import LogsService, UserService


class GetLog(APIView):

    def post(self, request, format=None):
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        count = LogsService(request, None).count()

        all_objects = Logs.objects.filter(isDeleted=False).filter(
            user__first_name__icontains=request.data['search[value]']).filter(
            user__last_name__icontains=request.data['search[value]']).order_by('-id')[
                      int(start):end]

        filteredTotal = Logs.objects.filter(isDeleted=False).filter(
            user__first_name__icontains=request.data['search[value]']).filter(
            user__last_name__icontains=request.data['search[value]']).count()

        serializer_context = {
            'request': request,

        }


class GetUser(APIView):

    def post(self, request, format=None):
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        globalSearch = request.data['search[value]']
        first_name = request.data['columns[1][search][value]']
        last_name = request.data['columns[2][search][value]']
        email = request.data['columns[3][search][value]']
        group = request.data['columns[4][search][value]']
        is_active = bool(request.data['columns[5][search][value]'])

        filter = {

            'is_superuser': False,
        }
        users = UserService(request, filter).exclude(email='')
        count = users.count()

        if not (first_name or last_name or email or group or is_active or globalSearch):
            all_objects = users.order_by('first_name')[int(start):end]
            filteredTotal = users.count()
        else:
            query = Q()
            if globalSearch:
                query &= Q(first_name__icontains=globalSearch.upper()) | Q(
                    last_name__icontains=globalSearch.upper()) | Q(
                    email__icontains=globalSearch.upper()) | Q(
                    groups__name__icontains=globalSearch.upper()) | \
                         Q(first_name__icontains=globalSearch.lower()) | Q(
                    last_name__icontains=globalSearch.lower()) | Q(
                    email__icontains=globalSearch.lower()) | Q(
                    groups__name__icontains=globalSearch.lower())
            if first_name:
                query &= Q(first_name__icontains=first_name.upper()) | \
                         Q(first_name__icontains=first_name.lower())
            if last_name:
                query &= Q(last_name__icontains=last_name.upper()) | \
                         Q(last_name__icontains=last_name.lower())
            if email:
                query &= Q(email__icontains=email.upper()) | \
                         Q(email__icontains=email.lower())
            if group:
                query &= Q(groups__pk=group.upper()) | \
                         Q(groups__pk=group.lower())

            all_objects = users.filter(query).order_by('first_name')[int(start):end]
            filteredTotal = users.filter(query).count()

        logApiObject = LogAPIObject()
        logApiObject.data = all_objects
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(count)
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,

        }
        serializer = UserResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)


class GetPermission(APIView):

    def post(self, request, format=None):
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        count = Permission.objects.filter(isDeleted=False).count()

        all_objects = Permission.objects.filter(isDeleted=False).filter(
            name__icontains=request.data['search[value]']).order_by('-creationDate')[
                      int(start):end]

        filteredTotal = Permission.objects.filter(isDeleted=False).filter(
            name__icontains=request.data['search[value]']).count()

        logApiObject = LogAPIObject()
        logApiObject.data = all_objects
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(count)
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,
        }
        serializer = PermissionResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)


class GetClub(APIView):

    def post(self, request, format=None):
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        globalSearch = request.data['search[value]']
        name = request.data['columns[1][search][value]']
        branch = request.data['columns[2][search][value]']
        city = request.data['columns[4][search][value]']
        count = Club.objects.all().exclude(name='').count()

        if not (name or branch or city or globalSearch):
            all_objects = Club.objects.all().exclude(name='').order_by('name')[int(start):end]
            filteredTotal = Club.objects.all().exclude(name='').count()
        else:
            query = Q()
            if globalSearch:
                query &= Q(name__icontains=globalSearch) | Q(
                    communication__city__name__icontains=globalSearch) | Q(
                    branch__title__icontains=globalSearch)
            if name:
                query &= Q(name__icontains=name)
            if city:
                query &= Q(communication__city__pk=city)
            if branch:
                query &= Q(branch__pk=branch)

            all_objects = Club.objects.filter(query).order_by('name')[int(start):end]
            filteredTotal = Club.objects.filter(query).count()

        logApiObject = LogAPIObject()
        logApiObject.data = all_objects
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(count)
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,

        }
        serializer = ClubResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)


class GetCoach(APIView):

    def post(self, request, format=None):
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        globalSearch = request.data['search[value]']
        first_name = request.data['columns[1][search][value]']
        last_name = request.data['columns[2][search][value]']
        email = request.data['columns[3][search][value]']
        city = request.data['columns[4][search][value]']
        branch = request.data['columns[5][search][value]']

        coaches = Coach.objects.none()

        coaches = Coach.objects.filter(isDeleted=False).order_by('-creationDate')
        count = coaches.count()

        if not (first_name or last_name or email or city or branch or globalSearch):
            all_objects = coaches.order_by('-creationDate')[int(start):end]
            filteredTotal = coaches.count()
        else:
            query = Q()
            if globalSearch:
                query &= Q(person__user__first_name__icontains=globalSearch.upper()) | Q(
                    person__user__last_name__icontains=globalSearch.upper()) | Q(
                    communication__city__name__icontains=globalSearch.upper()) | Q(
                    branch__title__icontains=globalSearch.upper()) | Q(
                    person__user__first_name__icontains=globalSearch.lower()) | Q(
                    person__user__last_name__icontains=globalSearch.lower()) | Q(
                    communication__city__name__icontains=globalSearch.lower()) | Q(
                    branch__title__icontains=globalSearch.lower())
            if first_name:
                query &= Q(person__user__first_name__icontains=first_name.upper()) | Q(
                    person__user__first_name__icontains=first_name.lower())
            if last_name:
                query &= Q(person__user__last_name__icontains=last_name.upper()) | Q(
                    person__user__last_name__icontains=last_name.lower())
            if email:
                query &= Q(person__user__email__icontains=email.upper()) | Q(
                    person__user__email__icontains=email.lower())
            if city:
                query &= Q(communication__city__pk=city)
            if branch:
                query &= Q(branch__pk=branch)

            all_objects = coaches.filter(query).order_by('-creationDate')[int(start):end]
            filteredTotal = coaches.filter(query).count()

        logApiObject = LogAPIObject()
        logApiObject.data = all_objects
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(count)
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,
        }
        serializer = CoachResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)


class GetReferenceCoach(APIView):

    def post(self, request, format=None):
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        globalSearch = request.data['search[value]']
        first_name = request.data['columns[1][search][value]']
        last_name = request.data['columns[2][search][value]']
        email = request.data['columns[3][search][value]']
        tc = request.data['columns[4][search][value]']
        status = request.data['columns[5][search][value]']

        coaches = ReferenceCoach.objects.none()

        coaches = ReferenceCoach.objects.filter(isDeleted=False).order_by('status')
        count = coaches.count()

        if not (first_name or last_name or email or tc or status or globalSearch):
            all_objects = coaches.order_by('status')[int(start):end]
            filteredTotal = coaches.count()
        else:
            query = Q()
            if globalSearch:
                query &= Q(first_name__icontains=globalSearch.upper()) | Q(
                    last_name__icontains=globalSearch.upper()) | Q(tc=globalSearch) | Q(
                    status__icontains=globalSearch.upper()) | Q(first_name__icontains=globalSearch.lower()) | Q(
                    last_name__icontains=globalSearch.lower()) | Q(status__icontains=globalSearch.lower()) | Q(
                    email__icontains=globalSearch.upper()) | Q(email__icontains=globalSearch.lower())
            if first_name:
                query &= Q(first_name__icontains=first_name.upper()) | Q(first_name__icontains=first_name.lower()) | Q(
                    first_name__contains=first_name) | Q(first_name__icontains=first_name.title())
            if last_name:
                query &= Q(last_name__icontains=last_name.upper()) | Q(last_name__icontains=last_name.lower()) | Q(
                    last_name__icontains=last_name.title())
            if email:
                query &= Q(email__icontains=email)
            if tc:
                query &= Q(tc__icontains=tc)
            if status:
                query &= Q(status__icontains=status)

            all_objects = coaches.filter(query).order_by('status')[int(start):end]
            filteredTotal = coaches.filter(query).count()

        logApiObject = LogAPIObject()
        logApiObject.data = all_objects
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(count)
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,
        }
        serializer = ReferenceCoachResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)


class GetCoachForVisaSeminar(APIView):

    def post(self, request, format=None):
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)
        uuid = request.POST['uuid']

        globalSearch = request.data['search[value]']
        first_name = request.data['columns[2][search][value]']
        last_name = request.data['columns[3][search][value]']
        tc = request.data['columns[4][search][value]']
        email = request.data['columns[5][search][value]']

        visa = VisaSeminar.objects.get(uuid=uuid)
        coa = []
        for item in visa.coach.all():
            coa.append(item.person.user.pk)
        coaches = Coach.objects.exclude(person__user__id__in=coa).filter(isDeleted=False).order_by(
            'person__user__first_name')
        count = coaches.count()

        if not (first_name or last_name or email or tc or globalSearch):
            all_objects = coaches.order_by('person__user__first_name')[int(start):end]
            filteredTotal = coaches.count()
        else:
            query = Q()
            if globalSearch:
                query &= Q(person__user__first_name__icontains=globalSearch) | Q(
                    person__user__last_name__icontains=globalSearch) | Q(
                    person__tc__icontains=globalSearch) | Q(
                    person__user__email__icontains=globalSearch)
            if first_name:
                query &= Q(person__user__first_name__icontains=first_name)
            if last_name:
                query &= Q(person__user__last_name__icontains=last_name)
            if email:
                query &= Q(person__user__email__icontains=email)
            if tc:
                query &= Q(person__tc__icontains=tc)

            all_objects = coaches.filter(query).order_by('person__user__first_name')[int(start):end]
            filteredTotal = coaches.filter(query).count()

        logApiObject = LogAPIObject()
        logApiObject.data = all_objects
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(count)
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,
        }
        serializer = CoachResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)


class GetRefereeForVisaSeminar(APIView):

    def post(self, request, format=None):
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)
        uuid = request.POST['uuid']

        globalSearch = request.data['search[value]']
        first_name = request.data['columns[2][search][value]']
        last_name = request.data['columns[3][search][value]']
        tc = request.data['columns[4][search][value]']
        email = request.data['columns[5][search][value]']

        visa = VisaSeminar.objects.get(uuid=uuid)
        coa = []
        for item in visa.referee.all():
            coa.append(item.person.user.pk)
        referees = Referee.objects.exclude(person__user__id__in=coa).filter(isDeleted=False).order_by(
            'person__user__first_name')
        count = referees.count()

        if not (first_name or last_name or email or tc or globalSearch):
            all_objects = referees.order_by('person__user__first_name')[int(start):end]
            filteredTotal = referees.count()
        else:
            query = Q()
            if globalSearch:
                query &= Q(person__user__first_name__icontains=globalSearch) | Q(
                    person__user__last_name__icontains=globalSearch) | Q(
                    person__tc__icontains=globalSearch) | Q(
                    person__user__email__icontains=globalSearch)
            if first_name:
                query &= Q(person__user__first_name__icontains=first_name)
            if last_name:
                query &= Q(person__user__last_name__icontains=last_name)
            if email:
                query &= Q(person__user__email__icontains=email)
            if tc:
                query &= Q(person__tc__icontains=tc)

            all_objects = referees.filter(query).order_by('person__user__first_name')[int(start):end]
            filteredTotal = referees.filter(query).count()

        logApiObject = LogAPIObject()
        logApiObject.data = all_objects
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(count)
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,
        }
        serializer = RefereeResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)


class GetReferee(APIView):
    def post(self, request, format=None):
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        globalSearch = request.data['search[value]']
        first_name = request.data['columns[1][search][value]']
        last_name = request.data['columns[2][search][value]']
        email = request.data['columns[3][search][value]']
        city = request.data['columns[4][search][value]']
        branch = request.data['columns[5][search][value]']

        count = Referee.objects.filter(person__isnull=False).count()
        if not (first_name or last_name or city or email or globalSearch):
            all_objects = Referee.objects.filter(person__isnull=False).order_by('person__user__first_name')[
                          int(start):end]
            filteredTotal = Referee.objects.filter(person__isnull=False).count()
        else:
            query = Q()
            if globalSearch:
                query &= Q(person__user__first_name__icontains=globalSearch) | Q(
                    person__user__last_name__icontains=globalSearch) | Q(
                    communication__city__name__icontains=globalSearch) | Q(
                    person__user__email__icontains=globalSearch) | Q(
                    branch__title__icontains=globalSearch)
            if first_name:
                query &= Q(person__user__first_name__icontains=first_name)
            if last_name:
                query &= Q(person__user__last_name__icontains=last_name)
            if city:
                query &= Q(communication__city__pk=city)
            if email:
                query &= Q(person__user__email__icontains=email)
            if branch:
                query &= Q(branch__pk=branch)

            all_objects = Referee.objects.filter(person__isnull=False).filter(query).order_by(
                'person__user__first_name')[int(start):end]
            filteredTotal = Referee.objects.filter(person__isnull=False).filter(query).count()

        logApiObject = LogAPIObject()
        logApiObject.data = all_objects
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(count)
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,

        }
        serializer = RefereeResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)


class GetFacility(APIView):

    def post(self, request, format=None):
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        count = SportFacility.objects.filter(isDeleted=False).count()

        all_objects = SportFacility.objects.filter(isDeleted=False).filter(

            Q(name__icontains=request.data['search[value]']) | Q(
                communication__city__name__icontains=request.data['search[value]']) | Q(
                derbis__icontains=request.data['search[value]'])).order_by('-creationDate')[
                      int(start):end]

        filteredTotal = SportFacility.objects.filter(isDeleted=False).filter(
            Q(name__icontains=request.data['search[value]']) | Q(
                communication__city__name__icontains=request.data['search[value]']) | Q(
                derbis__icontains=request.data['search[value]'])).count()

        logApiObject = LogAPIObject()
        logApiObject.data = all_objects
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(count)
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,
        }
        serializer = SportFacilityResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)


@login_required
def SetPasswordAllUsers(request):
    try:
        with transaction.atomic():
            perm = general_methods.control_access(request)

            if not perm:
                logout(request)
                return redirect('accounts:login')

            password = User.objects.make_random_password()
            coaches = User.objects.filter(groups__name='Antrenör')
            timestr = time.strftime("%Y%m%d-%H%M%S")
            file_name = 'coaches-' + str(timestr) + '.csv'
            csv_file = open(file_name, "w", encoding='utf-8')
            csv_file.write('Name, Email, Password\n')
            for coach in coaches:
                coach.set_password(password)
                coach.save()
                if coach.first_name:
                    csv_file.write(str(coach.first_name) + ' ')
                if coach.last_name:
                    csv_file.write(str(coach.last_name) + ', ')
                else:
                    csv_file.write(', ')
                if coach.email:
                    csv_file.write(str(coach.email) + ', ')
                else:
                    csv_file.write(', ')
                if coach.password:
                    csv_file.write(password)
                else:
                    csv_file.write(' ')
                csv_file.write('\n')
            csv_file.close()

            messages.success(request, 'Tüm Antrenörlere Şifre Kaydı Yapıldı.')

            return redirect('sbs:view_admin')

    except Exception as e:
        messages.warning(request, e)
        traceback.print_exc()
        return redirect('sbs:view_admin')


def transmissionCoachTc(request):
    try:
        with transaction.atomic():
            if request.method == 'POST':
                tc = str(request.POST['tc'])
                result = TransmissionCoachDetail(request, tc)
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


def TransmissionCoachDetail(request, tc):
    try:
        with transaction.atomic():
            id = tc
            url = 'https://servis3.gsb.gov.tr/SporFedProtokol/api/FederasyonServisleri/FederasyonaGoreAntrenorBelgeDetayGetir?tc=' + id + ''

            payload = {}
            files = {}
            headers = {
                'Authorization': 'Basic dnVjdXRnZWxpc3Rpcm1lYWt0YXJpbTphMzE5YzczNC03ZjhlLTQ4NzQtYmExYy00YzU4MmU2NjExYTg='
            }

            response = requests.request("GET", url, headers=headers, data=payload, files=files)
            y = json.loads(response.text)
            result = []
            if y['Data']:
                return y['Data']


    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('sbs:return_clubs')


def GetCurrentRegister(request):
    try:
        with transaction.atomic():
            if request.method == 'POST':
                tcKimlikNo = request.POST['tcKimlikNo']
                info = 'ilk kayıt'
                if ReferenceCoach.objects.filter(tc=tcKimlikNo) or ReferenceCoach.objects.filter(email=tcKimlikNo):
                    if ReferenceCoach.objects.filter(tc=tcKimlikNo).count() > 1 or ReferenceCoach.objects.filter(
                            email=tcKimlikNo).count() > 1:
                        return JsonResponse(
                            {'status': 'Fail',
                             'msg': 'Sistemde birden fazla kaydınız bulunmaktadır. Lütfen yetkili ile görüşünüz.',
                             'result': info,
                             })
                    if ReferenceCoach.objects.filter(tc=tcKimlikNo):
                        register_info = ReferenceCoach.objects.get(tc=tcKimlikNo)
                    if ReferenceCoach.objects.filter(email=tcKimlikNo):
                        register_info = ReferenceCoach.objects.get(email=tcKimlikNo)
                    if register_info.status != 'Reddedildi':
                        return JsonResponse(
                            {'status': 'Fail',
                             'msg': 'Başvurunuz Daha Önceden Alınmıştır.Başvuru Onay Aşamasında Olduğu İçin Güncelleme Yapılamamaktadır.Lütfen kayıt yapılan mail adresinize gelecek maili bekleyin.',
                             'result': info,
                             })
                    date = register_info.birthDate
                    birthDate = datetime.datetime.strptime(str(date), "%Y-%m-%d").strftime("%d-%m-%Y")
                    if register_info.profileImage:
                        profileImage = register_info.profileImage.url
                    else:
                        profileImage = ''
                    if register_info.birthplace:
                        birthplace = register_info.birthplace
                    else:
                        birthplace = ''
                    if register_info.iban:
                        iban = register_info.iban
                    else:
                        iban = ''
                    if register_info.club:
                        club = register_info.club.name
                    else:
                        club = ''
                    if register_info.city:
                        city = register_info.city.name
                    else:
                        city = ''
                    if register_info.country:
                        country = register_info.country.name
                    else:
                        country = ''

                    if register_info.kademe_definition:
                        kademe_definition = register_info.kademe_definition.name
                    else:
                        kademe_definition = ''
                    if register_info.kademe_brans:
                        kademe_brans = register_info.kademe_brans.title
                    else:
                        kademe_brans = ''
                    if register_info.belge:
                        belge = register_info.belge.url
                    else:
                        belge = ''

                    if register_info.kademe_definition2:
                        kademe_definition2 = register_info.kademe_definition2.name
                    else:
                        kademe_definition2 = ''
                    if register_info.kademe_brans2:
                        kademe_brans2 = register_info.kademe_brans2.title
                    else:
                        kademe_brans2 = ''
                    if register_info.belge2:
                        belge2 = register_info.belge2.url
                    else:
                        belge2 = ''

                    if register_info.vize_brans:
                        vize_brans = register_info.vize_brans.title
                    else:
                        vize_brans = ''
                    if register_info.dekont:
                        dekont = register_info.dekont.url
                    else:
                        dekont = ''

                    if register_info.vize_brans2:
                        vize_brans2 = register_info.vize_brans2.title
                    else:
                        vize_brans2 = ''
                    if register_info.dekont2:
                        dekont2 = register_info.dekont2.url
                    else:
                        dekont2 = ''

                    if register_info.kademe_belge:
                        kademe_belge = register_info.kademe_belge.url
                    else:
                        kademe_belge = ''
                    if register_info.sgk:
                        sgk = register_info.sgk.url
                    else:
                        sgk = ''
                    if register_info.definition:
                        definition = register_info.definition
                    else:
                        definition = ''
                    if register_info.phoneNumber:
                        phoneNumber = register_info.phoneNumber
                    else:
                        phoneNumber = ''
                    if register_info.phoneNumber2:
                        phoneNumber2 = register_info.phoneNumber2
                    else:
                        phoneNumber2 = ''
                    if register_info.address:
                        address = register_info.address
                    else:
                        address = ''

                    info = {}
                    info['profilImage'] = profileImage
                    info['first_name'] = register_info.first_name
                    info['last_name'] = register_info.last_name
                    info['birthplace'] = birthplace
                    info['iban'] = iban
                    info['kademe_belge'] = kademe_belge
                    info['sgk'] = sgk
                    info['birthDate'] = birthDate
                    info['gender'] = register_info.gender
                    info['club'] = club
                    info['email'] = register_info.email
                    info['country'] = country
                    info['phoneNumber'] = phoneNumber
                    info['city'] = city
                    info['phoneNumber2'] = phoneNumber2
                    info['address'] = address

                    info['kademe_definition'] = kademe_definition
                    info['kademe_brans'] = kademe_brans
                    info['belge'] = belge

                    info['kademe_definition2'] = kademe_definition2
                    info['kademe_brans2'] = kademe_brans2
                    info['belge2'] = belge2

                    info['vize_brans'] = vize_brans
                    info['dekont'] = dekont

                    info['vize_brans2'] = vize_brans2
                    info['dekont2'] = dekont2

                    info['definition'] = definition
                    info['tc'] = register_info.tc

                if info:
                    return JsonResponse({'status': 'Success',
                                         'msg': 'Bu bilgiye ait bir kayıt bulunamadı. Kayıt olmak için formu doldurunuz.',
                                         'result': info,
                                         })
                else:
                    return JsonResponse(
                        {'status': 'Fail',
                         'msg': 'Bu bilgiye ait bir kayıt bulunamadı. Kayıt olmak için formu doldurunuz.',
                         'result': info,
                         })

    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('accounts:coach')


class GetReferenceReferee(APIView):

    def post(self, request, format=None):
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        globalSearch = request.data['search[value]']
        first_name = request.data['columns[1][search][value]']
        last_name = request.data['columns[2][search][value]']
        email = request.data['columns[3][search][value]']
        tc = request.data['columns[4][search][value]']
        status = request.data['columns[5][search][value]']

        referees = ReferenceReferee.objects.filter(isDeleted=False).order_by('status')
        count = referees.count()

        if not (first_name or last_name or email or tc or status or globalSearch):
            all_objects = referees.order_by('status')[int(start):end]
            filteredTotal = referees.count()
        else:
            query = Q()
            if globalSearch:
                query &= Q(first_name__icontains=globalSearch) | Q(
                    last_name__icontains=globalSearch) | Q(
                    tc=globalSearch) | Q(
                    status__icontains=globalSearch)
            if first_name:
                query &= Q(first_name__icontains=first_name)
            if last_name:
                query &= Q(last_name__icontains=last_name)
            if email:
                query &= Q(email__icontains=email)
            if tc:
                query &= Q(tc__icontains=tc)
            if status:
                query &= Q(status__icontains=status)

            all_objects = referees.filter(query).order_by('status')[int(start):end]
            filteredTotal = referees.filter(query).count()

        logApiObject = LogAPIObject()
        logApiObject.data = all_objects
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(count)
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,
        }
        serializer = ReferenceRefereeResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)


def GetCurrentRegisterReferee(request):
    try:
        with transaction.atomic():
            if request.method == 'POST':
                tcKimlikNo = request.POST['tcKimlikNo']
                info = 'ilk kayıt'
                if ReferenceReferee.objects.filter(tc=tcKimlikNo) or ReferenceReferee.objects.filter(email=tcKimlikNo):
                    if ReferenceReferee.objects.filter(tc=tcKimlikNo).count() > 1 or ReferenceReferee.objects.filter(
                            email=tcKimlikNo).count() > 1:
                        return JsonResponse(
                            {'status': 'Fail',
                             'msg': 'Sistemde birden fazla kaydınız bulunmaktadır. Lütfen yetkili ile görüşünüz.',
                             'result': info,
                             })
                    if ReferenceReferee.objects.filter(tc=tcKimlikNo):
                        referee = ReferenceReferee.objects.get(tc=tcKimlikNo)
                    if ReferenceReferee.objects.filter(email=tcKimlikNo):
                        referee = ReferenceReferee.objects.get(email=tcKimlikNo)
                    if referee.status != 'Reddedildi':
                        return JsonResponse(
                            {'status': 'Fail',
                             'msg': 'Başvurunuz Daha Önceden Alınmıştır.Başvuru Onay Aşamasında Olduğu İçin Güncelleme Yapılamamaktadır.Lütfen kayıt yapılan mail adresinize gelecek maili bekleyin.',
                             'result': info,
                             })
                    date = referee.birthDate
                    birthDate = datetime.datetime.strptime(str(date), "%Y-%m-%d").strftime("%d-%m-%Y")

                    date2 = referee.gradeDate
                    gradeDate = datetime.datetime.strptime(str(date2), "%Y-%m-%d").strftime("%d-%m-%Y")

                    if referee.profileImage:
                        profileImage = referee.profileImage.url
                    else:
                        profileImage = ''
                    if referee.referee_file:
                        referee_file = referee.referee_file.url
                    else:
                        referee_file = ''
                    if referee.birthplace:
                        birthplace = referee.birthplace
                    else:
                        birthplace = ''
                    if referee.iban:
                        iban = referee.iban
                    else:
                        iban = ''
                    if referee.city:
                        city = referee.city.name
                    else:
                        city = ''
                    if referee.country:
                        country = referee.country.name
                    else:
                        country = ''
                    if referee.kademe_definition:
                        kademe_definition = referee.kademe_definition.name
                    else:
                        kademe_definition = ''
                    if referee.grade_referee_contract:
                        grade_referee_contract = referee.grade_referee_contract.url
                    else:
                        grade_referee_contract = ''
                    if referee.sgk:
                        sgk = referee.sgk.url
                    else:
                        sgk = ''
                    if referee.dekont:
                        dekont = referee.dekont.url
                    else:
                        dekont = ''
                    if referee.definition:
                        definition = referee.definition
                    else:
                        definition = ''
                    if referee.phoneNumber:
                        phoneNumber = referee.phoneNumber
                    else:
                        phoneNumber = ''
                    if referee.phoneNumber2:
                        phoneNumber2 = referee.phoneNumber2
                    else:
                        phoneNumber2 = ''
                    if referee.address:
                        address = referee.address
                    else:
                        address = ''
                    if referee.gradeNo:
                        gradeNo = referee.gradeNo
                    else:
                        gradeNo = ''

                    info = {}
                    info['profilImage'] = profileImage
                    info['first_name'] = referee.first_name
                    info['last_name'] = referee.last_name
                    info['birthplace'] = birthplace
                    info['iban'] = iban
                    info['referee_file'] = referee_file
                    info['birthDate'] = birthDate
                    info['gender'] = referee.gender
                    info['email'] = referee.email
                    info['country'] = country
                    info['phoneNumber'] = phoneNumber
                    info['city'] = city
                    info['phoneNumber2'] = phoneNumber2
                    info['address'] = address
                    info['kademe_definition'] = kademe_definition
                    info['grade_referee_contract'] = grade_referee_contract
                    info['sgk'] = sgk
                    info['dekont'] = dekont
                    info['definition'] = definition
                    info['gradeNo'] = gradeNo
                    info['gradeDate'] = gradeDate

                if info:
                    return JsonResponse({'status': 'Success',
                                         'msg': 'Bu bilgiye ait bir kayıt bulunamadı. Kayıt olmak için formu doldurunuz.',
                                         'result': info,
                                         })
                else:
                    return JsonResponse(
                        {'status': 'Fail', 'msg': 'Bu Tc kimlik  numarasına ait bir kayıt bulunamadı.',
                         'result': info,
                         })

    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('accounts:referee')


class GetGradeList(APIView):

    def post(self, request, format=None):
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        globalSearch = request.data['search[value]']

        grades = HavaLevel.objects.filter(levelType=EnumFields.LEVELTYPE.GRADE).order_by('status')
        count = grades.count()

        if not globalSearch:
            all_objects = grades.order_by('status')[int(start):end]
            filteredTotal = grades.count()
        else:
            query = Q()
            if globalSearch:
                query &= Q(branch__title__icontains=globalSearch.upper()) | Q(
                    status__icontains=globalSearch.upper()) | Q(branch__title__icontains=globalSearch.lower()) | Q(
                    status__icontains=globalSearch.lower())

            all_objects = grades.filter(query).order_by('status')[int(start):end]
            filteredTotal = grades.filter(query).count()

        gradeList = []
        counter = 0
        for item in all_objects:
            if item.CoachGrades:
                name = item.CoachGrades.first()
            else:
                name = ''
            if item.branch:
                branch = item.branch.title
            else:
                branch = ''
            if item.startDate:
                startDate = item.startDate
            else:
                startDate = ''
            if item.status:
                status = item.status
            else:
                status = ''
            if item.approval_date:
                approvalDate = item.approval_date
            else:
                approvalDate = ''
            if item.definition:
                definition = item.definition.name
            else:
                definition = ''
            if item.dekont:
                dekontName = item.dekont
                dekontUrl = item.dekont.url
            else:
                dekontName = ''
                dekontUrl = ''
            grade = {
                'counter': counter,
                'name': str(name),
                'branch': str(branch),
                'startDate': str(startDate),
                'status': str(status),
                'approvalDate': str(approvalDate),
                'definition': str(definition),
                'dekontUrl': str(dekontUrl),
                'dekontName': str(dekontName),
                'uuid': str(item.uuid),
            }
            gradeList.append(grade)
            counter += 1

        response = {

            'data': gradeList,
            'draw': draw,
            'recordsTotal': int(count),
            'recordsFiltered': int(filteredTotal),
        }

        return JsonResponse(response)

def GradeTransmission(request):
    try:
        with transaction.atomic():
            coachTc = Coach.objects.filter(creationDate__gte='2022-07-05').filter(grades__isnull=True).values('person__tc')
            referenceCoaches = ReferenceCoach.objects.filter(tc__in=coachTc)
            for referenceCoach in referenceCoaches:
                coach = Coach.objects.get(person__tc=referenceCoach.tc)
                approvalDate = datetime.datetime.strptime('2022-07-07', '%Y-%m-%d').date()
                if referenceCoach.kademe_definition and referenceCoach.belge:
                    grade = HavaLevel(definition=referenceCoach.kademe_definition,
                                      antrenorBelgesi=referenceCoach.belge,
                                      branch=Branch.objects.get(title='VÜCUT GELİŞTİRME VE FİTNESS'))
                    grade.levelType = EnumFields.LEVELTYPE.GRADE
                    grade.status = HavaLevel.APPROVED
                    grade.isActive = True
                    grade.approval_date = approvalDate
                    grade.save()
                    coach.grades.add(grade)
                if referenceCoach.kademe_definition2 and referenceCoach.belge2:
                    grade2 = HavaLevel(definition=referenceCoach.kademe_definition2,
                                      antrenorBelgesi=referenceCoach.belge2,
                                      branch=Branch.objects.get(title='BİLEK GÜREŞİ'))
                    grade2.levelType = EnumFields.LEVELTYPE.GRADE
                    grade2.status = HavaLevel.APPROVED
                    grade2.isActive = True
                    grade2.approval_date = approvalDate
                    grade2.save()
                    coach.grades.add(grade2)
                if referenceCoach.dekont:
                    visa = HavaLevel(dekont=referenceCoach.dekont, branch=Branch.objects.get(title='VÜCUT GELİŞTİRME VE FİTNESS'))
                    visa.levelType = EnumFields.LEVELTYPE.VISA
                    visa.status = HavaLevel.APPROVED
                    visa.isActive = True
                    visa.approval_date = approvalDate
                    visa.save()
                    coach.visa.add(visa)
                if referenceCoach.dekont2:
                    visa2 = HavaLevel(dekont=referenceCoach.dekont2, branch=Branch.objects.get(title='BİLEK GÜREŞİ'))
                    visa2.levelType = EnumFields.LEVELTYPE.VISA
                    visa2.status = HavaLevel.APPROVED
                    visa2.isActive = True
                    visa2.approval_date = approvalDate
                    visa2.save()
                    coach.visa.add(visa2)
                referenceCoach.status = referenceCoach.APPROVED
                referenceCoach.save()
            messages.success(request, 'işlem yapıldı.')
            return redirect('sbs:view_admin')


    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('sbs:view_admin')
