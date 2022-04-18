import traceback

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import resolve

from sbs.models import Club, SportClubUser, Coach, Referee, Person
from sbs.models.ekabis.City import City
from sbs.models.ekabis.Permission import Permission
from sbs.models.tvfbf.Athlete import Athlete
from sbs.services import general_methods
from sbs.services.services import ActiveGroupGetService, GroupGetService, \
     last_urls, \
    YekaGetService, YekaCompetitionGetService

import datetime

from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers


@login_required
def return_directory_dashboard(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    return render(request, 'anasayfa/federasyon.html',
                  {

                  })



@login_required
def return_club_user_dashboard(request):


    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    current_user = request.user
    clubuser = SportClubUser.objects.get(user=current_user)
    club = Club.objects.filter(clubUser=clubuser)[0]


    total_club_user = club.clubUser.count()
    total_coach = club.coachs.all().count()
    sc_user = SportClubUser.objects.get(user=user)
    clubsPk = []
    clubs = Club.objects.filter(clubUser=sc_user)
    for club in clubs:
        clubsPk.append(club.pk)
    total_athlete = Athlete.objects.filter(club__in=clubsPk).distinct().count()

    # Sporcu bilgilerinde eksik var mı diye control
    athletes = Athlete.objects.none()
    if user.groups.filter(name='Kulüp Yetkilisi'):
        sc_user = SportClubUser.objects.get(user=user)
        if sc_user.dataAccessControl == False or sc_user.dataAccessControl == None:
            clubsPk = []
            clubs = Club.objects.filter(clubUser=sc_user)
            for club in clubs:
                if club.dataAccessControl == False or club.dataAccessControl is None:
                    clubsPk.append(club.pk)

            if len(clubsPk) != 0:
                athletes = Athlete.objects.filter(club__in=clubsPk).distinct()
                athletes = athletes.filter(person__user__last_name='') | athletes.filter(person__user__first_name='') | athletes.filter(
                    person__user__email='') | athletes.filter(person__tc='') | athletes.filter(
                    person__birthDate=None) | athletes.filter(
                    person__gender=None) | athletes.filter(person__birthplace='') | athletes.filter(
                    person__motherName='') | athletes.filter(person__fatherName='') | athletes.filter(
                    communication__city__name='') | athletes.filter(communication__country__name='')
                # false degerinde clubun eksigi yok anlamında kulanilmistir.
                for club in clubs:
                    if athletes:
                        club.dataAccessControl = False
                        club.save()

                    else:

                        club.dataAccessControl = True
                        club.save()


                if athletes:
                    sc_user.dataAccessControl = False

                else:
                    sc_user.dataAccessControl = True

                sc_user.save()


            else:
                sc_user.dataAccessControl = True
                sc_user.save()

    return render(request, 'TVGFBF/Anasayfa/kulup-uyesi.html',
                  {'total_club_user': total_club_user, 'total_coach': total_coach,
                   'total_athlete': total_athlete, 'athletes': athletes,
                   'urls': urls, 'current_url': current_url, 'url_name': url_name})

@login_required
def return_referee_dashboard(request):
    # perm = general_methods.control_access_judge(request)
    #
    # if not perm:
    #     logout(request)
    #     return redirect('accounts:login')
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    user = User.objects.get(pk=request.user.pk)
    judge = Referee.objects.get(user=user)
    return render(request, 'TVGFBF/Anasayfa/hakem.html', {'user': user, 'judge': judge,
                                                   'urls': urls, 'current_url': current_url, 'url_name': url_name})


@login_required
def return_admin_dashboard(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    last_athlete = Athlete.objects.order_by('-creationDate')[:8]
    total_club = Club.objects.all().count()
    total_athlete = Athlete.objects.all().count()
    total_athlete_gender_man = Athlete.objects.filter(person__gender=Person.MALE).count()
    total_athlete_gender_woman = Athlete.objects.filter(person__gender=Person.FEMALE).count()
    total_athlate_last_month = Athlete.objects.exclude(person__user__date_joined__month=datetime.datetime.now().month).count()
    total_club_user = SportClubUser.objects.all().count()
    total_coachs = Coach.objects.all().count()
    total_judge = Referee.objects.all().count()
    total_user = User.objects.all().count()

    return render(request, 'TVGFBF/Anasayfa/admin.html',
                  {'total_club_user': total_club_user, 'total_club': total_club,
                   'total_athlete': total_athlete, 'total_coachs': total_coachs, 'last_athletes': last_athlete,
                   'total_athlete_gender_man': total_athlete_gender_man,
                   'total_athlete_gender_woman': total_athlete_gender_woman,
                   'total_athlate_last_month': total_athlate_last_month,
                   'total_judge': total_judge, 'total_user': total_user,
                   'urls': urls, 'current_url': current_url, 'url_name': url_name})


def City_athlete_cout(request):

    if request.method == 'POST' and request.is_ajax():
        try:
            cityName = str(request.POST.get('city')).upper()
            coachcout = Coach.objects.filter(communication__city__name__icontains=cityName).count()
            refereecout = Referee.objects.filter(communication__city__name__icontains=cityName).count()
            sportsClub = Club.objects.filter(
                communication__city__name__icontains=cityName).count()

            response = JsonResponse({
                'coach': coachcout,
                'referee': refereecout,
                'sportsClub': sportsClub
            })

            return response
        except:
            response = JsonResponse({
                'success': 'GET',
            })
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            response["Access-Control-Max-Age"] = "1000"
            response["Access-Control-Allow-Headers"] = "*"
            return response

    else:
        response = JsonResponse({
            'success': 'GET',
        })
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return  response


@login_required
def activeGroup(request, pk):
    activefilter = {
        'user': request.user
    }
    userActive = ActiveGroupGetService(request, activefilter)
    groupfilter = {
        'pk': pk
    }
    group = GroupGetService(request, groupfilter)
    userActive.group = group
    userActive.save()
    if group.name == "Admin":
        return redirect('sbs:view_admin')

    elif group.name == 'Yönetici':
        return redirect('sbs:view_federasyon')
    elif group.name == 'Hakem':
        return redirect('sbs:view_personel')
    elif group.name == 'Antrenör':
        return redirect('sbs:view_personel')
    else:
        logout(request)
        return redirect('accounts:404')



def add_calendar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.GET['uuid']
                date = request.GET['date']

                datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S'").date()

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def api_connection_region_cities(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                yekafilter = {
                    'uuid': uuid
                }
                array = []
                yeka = YekaGetService(request, yekafilter)
                cities = City.objects.filter(connectionregion__id__in=yeka.connection_region.all().values_list('pk'))
                cities = serializers.serialize("json", cities, cls=DjangoJSONEncoder)
                regions = serializers.serialize("json", yeka.connection_region.all(), cls=DjangoJSONEncoder)
                array.append(cities)
                array.append(regions)
                return JsonResponse({'status': 'Success', 'msg': 'İşlem Başarılı', 'cities': array})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})




def success_initial_data(request):
    return render(request, 'anasayfa/initial_data_success.html')


def error_initial_data(request):
    return render(request, 'anasayfa/initial_data_error.html')


