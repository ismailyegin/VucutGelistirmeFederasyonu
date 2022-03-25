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
from sbs.models.ekabis.CalendarName import CalendarName
from sbs.models.ekabis.CalendarYeka import CalendarYeka
from sbs.models.ekabis.City import City
from sbs.models.ekabis.ConnectionRegion import ConnectionRegion
from sbs.models.ekabis.Permission import Permission
from sbs.models.ekabis.Yeka import Yeka
from sbs.models.ekabis.YekaAccept import YekaAccept
from sbs.models.ekabis.YekaCompetition import YekaCompetition
from sbs.models.ekabis.YekaContract import YekaContract
from sbs.models.tvfbf.Athlete import Athlete
from sbs.services import general_methods
from sbs.services.services import ActiveGroupGetService, GroupGetService, \
    CalendarNameService, YekaService, VacationDayService, ConnectionRegionService, last_urls, EmployeeGetService, \
    YekaCompetitionPersonService, YekaGetService, YekaCompetitionGetService

from sbs.Forms.CalendarNameForm import CalendarNameForm
from django.contrib import messages
import datetime

from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers


@login_required
def return_directory_dashboard(request):
    # perm = general_methods.control_access(request)
    # if not perm:
    #     logout(request)
    #     return redirect('accounts:login')

    return render(request, 'TVGFBF/Anasayfa/federasyon.html',
                  {

                  })




@login_required
def return_personel_dashboard(request):
    active = general_methods.controlGroup(request)
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')



    return render(request, 'anasayfa/personel.html', {})


@login_required
def return_yonetici_dashboard(request):
    active = general_methods.controlGroup(request)
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    calendar_filter = {
        'isDeleted': False,
        'user': request.user
    }

    calendarNames = CalendarNameService(request, calendar_filter)
    yekas = YekaService(request, None).order_by('-date')
    comp_array = []
    competitions = []
    for yeka in yekas:
        yeka_dict = dict()
        regions = yeka.connection_region.filter(isDeleted=False)
        for region in regions:
            for comp in region.yekacompetition.filter(isDeleted=False):
                comp_dict = dict()
                comp_dict['pk'] = comp.pk
                comp_dict['competition'] = '(' + yeka.definition + ')' + ' - ' + comp.name
                competitions.append(comp_dict)
        yeka_dict['yeka'] = yeka
        yeka_dict['regions'] = regions
        comp_array.append(yeka_dict)

    yeka_accept_array = []
    for yeka in yekas:
        accept_array = []
        accept_dict = dict()
        accept_dict['yeka'] = yeka
        for region in yeka.connection_region.filter(isDeleted=False):
            for competition in region.yekacompetition.filter(isDeleted=False):
                yeka_accepts = YekaAccept.objects.filter(business=competition.business).filter(isDeleted=False)
                if yeka_accepts:
                    yeka_accept = YekaAccept.objects.get(business=competition.business, isDeleted=False)
                    for accept in yeka_accept.accept.filter(isDeleted=False):
                        accept_array.append(accept)
        accept_dict['accepts'] = accept_array
        yeka_accept_array.append(accept_dict)

    yeka_capacity_array = []
    for yeka_accept in yeka_accept_array:

        yeka_capacity_dict = dict()
        yeka_capacity_dict['label'] = yeka_accept['yeka'].definition
        total_installed = 0
        total_current = 0
        for accept in yeka_accept['accepts']:
            total_installed += float(accept.installedPower)
            total_current += float(accept.currentPower)
        capacity_total = round(float(total_current), 3)
        yeka_capacity_dict['remaining_capacity'] = round(yeka_accept['yeka'].capacity - round(float(capacity_total), 3),
                                                         3)
        yeka_capacity_dict['total'] = yeka_accept['yeka'].capacity
        yeka_capacity_dict['capacity'] = capacity_total
        if not yeka_capacity_dict in yeka_capacity_array:
            yeka_capacity_array.append(yeka_capacity_dict)
    days = VacationDayService(request, None)

    res_count = yekas.filter(type='Rüzgar').count()
    ges_count = yekas.filter(type='Güneş').count()
    biyo_count = yekas.filter(type='Biyokütle').count()
    jeo_count = yekas.filter(type='Jeotermal').count()

    regions = ConnectionRegionService(request, None)

    return render(request, 'TVGFBF/Anasayfa/federasyon.html',
                  {'res_count': res_count, 'yeka': yekas, 'vacation_days': days,
                   'ges_count': ges_count, 'yekas': comp_array,'regions':regions,
                   'jeo_count': jeo_count, 'biyo_count': biyo_count, 'yeka_capacity': yeka_capacity_array,
                   'calendarNames': calendarNames, 'competitions': competitions,
                   })


@login_required
def return_coach_dashboard(request):
    perm = general_methods.control_access_klup(request)
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    coach=None
    athlete_count=0
    if Coach.objects.filter(person__user=user):
        coach = Coach.objects.get(person_user=user)
        clup = Club.objects.filter(coachs=coach)
        clupsPk = []
        for item in clup:
            clupsPk.append(item.pk)
        athletes = Athlete.objects.filter(licenses__sportsClub_id__in=clupsPk).distinct()
        athletes |= Athlete.objects.filter(licenses__coach=coach).distinct()

        athlete_count = athletes.count()

    return render(request, 'TVGFBF/Anasayfa/antrenor.html', {'athlete_count': athlete_count})

@login_required
def return_club_user_dashboard(request):


    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    current_user = request.user
    total_club_user=0
    total_coach=0
    athletes=None
    total_athlete=0
    coachs=None
    clubUsers=None
    if SportClubUser.objects.filter(user=current_user):
        clubuser = SportClubUser.objects.get(user=current_user)
        club = Club.objects.filter(clubUser=clubuser)[0]


        total_club_user = club.clubUser.count()
        total_coach = club.coachs.all().count()
        coachs=club.coachs.all()
        clubUsers=club.clubUser.all()
        sc_user = SportClubUser.objects.get(user=user)
        clubsPk = []
        clubs = Club.objects.filter(clubUser=sc_user)
        for club in clubs:
            clubsPk.append(club.pk)
        # total_athlete = Athlete.objects.filter(club__in=clubsPk).distinct().count()

    return render(request, 'TVGFBF/Anasayfa/kulup-uyesi.html',
                  {'total_club_user': total_club_user, 'total_coach': total_coach,
                   'total_athlete': total_athlete, 'athletes': athletes,'coachs':coachs,'clubUsers':clubUsers,
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
    judge=None
    visa=None
    if Referee.objects.filter(person__user=user):
        judge=Referee.objects.get(person__user=user)


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

    elif group.name == 'Yönetim':
        return redirect('sbs:view_federasyon')
    elif group.name == 'Hakem':
        return redirect('sbs:hakem')
    elif group.name == 'Antrenör':
        return redirect('sbs:antrenor')
    elif group.name == 'Kulüp Yetkilisi':
        return redirect('sbs:kulup-uyesi')
    else:
        logout(request)
        return redirect('accounts:404')


@login_required()
def add_calendarName(request):
    calender_form = CalendarNameForm()

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':
                calender_form = CalendarNameForm(request.POST)
                if calender_form.is_valid():
                    name = calender_form.save(request, commit=False)
                    name.user = request.user
                    name.save()
            calenders = CalendarName.objects.filter(isDeleted=False)
            return render(request, 'anasayfa/CalendarNameAdd.html',
                          {
                              'calender_form': calender_form,
                              'calanders': calenders, 'urls': urls,
                              'current_url': current_url, 'url_name': url_name
                          })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


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


@login_required
def api_yeka_by_type(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                type = request.POST['type']

                regions = ConnectionRegion.objects.filter(yeka__type=type).values('cities__plateNo').annotate(
                    count=Count('cities__id'))
                array = []
                for region in regions:
                    yeka_dict = dict()
                    yeka_dict['city'] = region['cities__plateNo']
                    yeka_dict['count'] = region['count']
                    array.append(yeka_dict)

                return JsonResponse({'status': 'Success', 'msg': 'İşlem Başarılı', 'yeka_type_cities': array})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def api_connection_region_competitions(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                yeka = None
                competitions = {}

                if request.POST['uuid']:
                    uuid = request.POST['uuid']
                    yekafilter = {
                        'uuid': uuid
                    }
                    yeka = YekaGetService(request, yekafilter)
                if request.POST['plateNo']:
                    if City.objects.filter(plateNo=request.POST['plateNo']):
                        city = City.objects.get(plateNo=request.POST['plateNo'])
                        if yeka:
                            regions = yeka.connection_region.filter(cities=city,
                                                                    isDeleted=False).distinct().values_list('id',
                                                                                                            flat=True)
                        else:
                            regions = ConnectionRegion.objects.filter(cities=city,
                                                                      isDeleted=False).distinct().values_list('id',
                                                                                                              flat=True)
                        competitions = YekaCompetition.objects.filter(competition_regions__id__in=regions,
                                                                      isDeleted=False).distinct()
                        competition_array=[]
                        for competition in competitions:
                            yeka_dict=dict()
                            yeka_dict['competition_id']=competition.uuid
                            yeka_dict['competition']=competition.name
                            region=ConnectionRegion.objects.filter(yekacompetition=competition)
                            if region:
                                region = ConnectionRegion.objects.get(yekacompetition=competition)
                                yeka=Yeka.objects.get(connection_region=region)
                                yeka_dict['yeka']=yeka.definition
                            else:
                                yeka_dict['yeka']=''
                            competition_array.append(yeka_dict)



                return JsonResponse({'status': 'Success', 'msg': 'İşlem Başarılı', 'competitions': competition_array})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request', 'competitions': []})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


def success_initial_data(request):
    return render(request, 'anasayfa/initial_data_success.html')


def error_initial_data(request):
    return render(request, 'anasayfa/initial_data_error.html')


@login_required
def api_yeka_accept(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                pk = request.POST['pk']
                yekafilter = {
                    'pk': pk
                }
                accept_dict = dict()
                currentPower_array = []
                yeka = YekaCompetitionGetService(request, yekafilter)
                yeka_acccepts = YekaAccept.objects.filter(isDeleted=False).filter(business=yeka.business).filter(
                    accept__isDeleted=False)
                accept_dict['label'] = 'Tamamlanan'
                total = yeka_acccepts.aggregate(Sum('accept__currentPower'))
                installed = yeka_acccepts.aggregate(Sum('accept__installedPower'))
                if total['accept__currentPower__sum'] is None:
                    total['accept__currentPower__sum'] = 0
                accept_dict['power'] = round(float(total['accept__currentPower__sum']), 2)
                currentPower_array.append(accept_dict)
                yeka_total = dict()
                yeka_total['label'] = 'Kalan'
                yeka_total['power'] = round((float(yeka.capacity) - accept_dict['power']), 3)
                currentPower_array.append(yeka_total)

                return JsonResponse({'status': 'Success', 'msg': 'İşlem Başarılı', 'accepts': currentPower_array})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request', 'accepts': []})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist', 'accepts': []})
