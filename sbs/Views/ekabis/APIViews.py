import time
import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
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
from sbs.services import general_methods
from sbs.services.services import LogsService


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
            coaches = User.objects.filter(groups__name='Antrenör').order_by('first_name')[:500]
            coachesCount = User.objects.filter(groups__name='Antrenör').order_by('first_name').count()
            timestr = time.strftime("%Y%m%d-%H%M%S")
            file_name = 'coaches-' + str(timestr) + '.txt'
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write('Name, Email, Password\n')
                for coach in coaches:
                    coach.set_password(str(password))
                    coach.save()
                    if coach.first_name:
                        f.write(str(coach.first_name) + ' ')
                    if coach.last_name:
                        f.write(str(coach.last_name) + ', ')
                    else:
                        f.write(', ')
                    if coach.email:
                        f.write(str(coach.email) + ', ')
                    else:
                        f.write(', ')
                    if coach.password:
                        f.write(str(password))
                    else:
                        f.write(' ')
                    f.write('\n')

            messages.success(request, 'Tüm Antrenörlere Şifre Kaydı Yapıldı.')

            return redirect('sbs:view_admin')

    except Exception as e:
        messages.warning(request, e)
        traceback.print_exc()
        return redirect('sbs:view_admin')
