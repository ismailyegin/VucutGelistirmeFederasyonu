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

from sbs.models import Permission, Coach, Referee, SportFacility
from sbs.models.ekabis.Logs import Logs
from sbs.models.tvfbf.LogAPIObject import LogAPIObject
from sbs.serializers.CoachSerializers import CoachResponseSerializer
from sbs.serializers.LogSerializers import LogResponseSerializer
from sbs.serializers.PermissionSerializers import PermissionResponseSerializer
from sbs.serializers.RefereeSerializers import RefereeResponseSerializer
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
                query &= Q(first_name__icontains=globalSearch) | Q(
                    last_name__icontains=globalSearch) | Q(
                    email__icontains=globalSearch) | Q(
                    groups__name__icontains=globalSearch)
            if first_name:
                query &= Q(first_name__icontains=first_name)
            if last_name:
                query &= Q(last_name__icontains=last_name)
            if email:
                query &= Q(email__icontains=email)
            if group:
                query &= Q(groups__pk=group)

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


class GetCoach(APIView):

    def post(self, request, format=None):
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        count = Coach.objects.filter(isDeleted=False).count()

        all_objects = Coach.objects.filter(isDeleted=False).filter(
            person__user__first_name__icontains=request.data['search[value]']).order_by('-creationDate')[
                      int(start):end]

        filteredTotal = Coach.objects.filter(isDeleted=False).filter(
            person__user__first_name__icontains=request.data['search[value]']).count()

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


class GetReferee(APIView):

    def post(self, request, format=None):
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        count = Referee.objects.filter(isDeleted=False).count()

        all_objects = Referee.objects.filter(isDeleted=False).filter(
            person__user__first_name__icontains=request.data['search[value]']).order_by('-creationDate')[
                      int(start):end]

        filteredTotal = Referee.objects.filter(isDeleted=False).filter(
            person__user__first_name__icontains=request.data['search[value]']).count()

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
            url = 'https://servis3.gsb.gov.tr/SporFedProtokol/api/FederasyonServisleri/FederasyonaGoreAntrenorBelgeDetayGetir?tc='+id+''

            payload = {}
            files = {}
            headers = {
                'Authorization': 'Basic dnVjdXRnZWxpc3Rpcm1lYWt0YXJpbTphMzE5YzczNC03ZjhlLTQ4NzQtYmExYy00YzU4MmU2NjExYTg='
            }

            response = requests.request("GET", url, headers=headers, data=payload, files=files)
            y = json.loads(response.text)
            result = []
            if y['Data']:
              return  y['Data']


    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return redirect('sbs:return_clubs')
