from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import resolve

from sbs.models.ekabis.Permission import Permission
from sbs.models.ekabis.Person import Person
from sbs.models.tvfbf.AnnouncementUser import AnnouncementUser
from sbs.models.tvfbf.Athlete import Athlete
from sbs.models.tvfbf.Club import Club
from sbs.models.tvfbf.Coach import Coach
from sbs.models.tvfbf.Referee import Referee
from sbs.models.tvfbf.SportClubUser import SportClubUser
from sbs.services import general_methods
from sbs.services.services import ActiveGroupGetService, GroupGetService, \
    last_urls

import datetime


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
def return_coach_dashboard(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    person = None
    if Person.objects.filter(user=user):
        person = Person.objects.get(user=user)
    coach = None
    clup = None
    athlete_count = 0
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    if Coach.objects.filter(person__user=user):
        coach = Coach.objects.get(person__user=user)
        clup = Club.objects.filter(coachs=coach)
        clupsPk = []
        for item in clup:
            clupsPk.append(item.pk)
        athletes = Athlete.objects.filter(club__id__in=clupsPk).distinct()
        # athletes |= Athlete.objects.filter(club__coachs__in=coach).distinct()

        athlete_count = athletes.count()

    return render(request, 'TVGFBF/Anasayfa/antrenor.html',
                  {'athlete_count': athlete_count, 'coach': coach, 'person': person, 'urls': urls,
                   'current_url': current_url, 'url_name': url_name, 'club': clup, })


@login_required
def return_club_user_dashboard(request):
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    current_user = request.user
    total_club_user = 0
    total_coach = 0
    athletes = None
    total_athlete = 0
    coachs = None
    clubUsers = None
    if SportClubUser.objects.filter(user=current_user):
        clubuser = SportClubUser.objects.get(user=current_user)
        club = Club.objects.filter(clubUser=clubuser)[0]

        total_club_user = club.clubUser.count()
        total_coach = club.coachs.all().count()
        coachs = club.coachs.all()
        clubUsers = club.clubUser.all()
        sc_user = SportClubUser.objects.get(user=user)
        clubsPk = []
        clubs = Club.objects.filter(clubUser=sc_user)
        for club in clubs:
            clubsPk.append(club.pk)
        # total_athlete = Athlete.objects.filter(club__in=clubsPk).distinct().count()

    return render(request, 'TVGFBF/Anasayfa/kulup-uyesi.html',
                  {'total_club_user': total_club_user, 'total_coach': total_coach,
                   'total_athlete': total_athlete, 'athletes': athletes, 'coachs': coachs, 'clubUsers': clubUsers,
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
    judge = None
    visa = None
    if Referee.objects.filter(person__user=user):
        judge = Referee.objects.get(person__user=user)

    return render(request, 'TVGFBF/Anasayfa/hakem.html', {'user': user, 'judge': judge,
                                                          'urls': urls, 'current_url': current_url,
                                                          'url_name': url_name})


@login_required
def return_admin_dashboard(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    last_coach = Coach.objects.order_by('-creationDate')[:4]
    last_referee = Referee.objects.order_by('-creationDate')[:4]

    total_club = Club.objects.all().count()
    total_athlete = Athlete.objects.all().count()
    total_athlete_gender_man = Athlete.objects.filter(person__gender=Person.MALE).count()
    total_athlete_gender_woman = Athlete.objects.filter(person__gender=Person.FEMALE).count()
    total_athlate_last_month = Athlete.objects.exclude(
        person__user__date_joined__month=datetime.datetime.now().month).count()
    total_club_user = SportClubUser.objects.all().count()
    total_coachs = Coach.objects.all().count()
    total_judge = Referee.objects.all().count()
    total_user = User.objects.all().count()

    return render(request, 'TVGFBF/Anasayfa/admin.html',
                  {'total_club_user': total_club_user, 'total_club': total_club,
                   'total_athlete': total_athlete, 'total_coachs': total_coachs, 'last_coaches': last_coach,
                   'total_athlete_gender_man': total_athlete_gender_man,
                   'total_athlete_gender_woman': total_athlete_gender_woman,
                   'total_athlate_last_month': total_athlate_last_month,
                   'total_judge': total_judge, 'total_user': total_user, 'last_referee': last_referee,
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
        return response


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
