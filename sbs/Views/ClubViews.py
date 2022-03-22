from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import resolve

from sbs.Forms.havaspor.ClubForm import ClubForm
from sbs.Forms.havaspor.ClupUserSearchForm import ClubSearchForm
from sbs.Forms.havaspor.CommunicationForm import CommunicationForm
from sbs.models import Club, SportClubUser, Coach, Communication
from sbs.models.ekabis.Permission import Permission
from sbs.models.havaspor.Athlete import Athlete
from sbs.services import general_methods
from sbs.services.services import last_urls


@login_required
def return_clubs(request):
    perm = general_methods.control_access_kulup(request)
    active = general_methods.controlGroup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    clubs = Club.objects.filter(infoStatus=1)
    ClupsSearchForm = ClubSearchForm(request.POST)
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    if request.method == 'POST':

        if ClupsSearchForm.is_valid():
            kisi = ClupsSearchForm.cleaned_data.get('kisi')
            branch = ClupsSearchForm.cleaned_data.get('branch')
            city = ClupsSearchForm.cleaned_data.get('city')
            name = ClupsSearchForm.cleaned_data.get('name')
            shortName = ClupsSearchForm.cleaned_data.get('shortName')
            clubMail = ClupsSearchForm.cleaned_data.get('clubMail')
            if not (kisi or city or name or shortName or clubMail or branch):
                if active == 'Kulüp Yetkilisi':
                    clubuser = SportClubUser.objects.get(user=user)
                    clubs = Club.objects.filter(clubUser=clubuser).order_by("-pk")
                elif active == 'Antrenör':
                    coach = Coach.objects.get(user=user)
                    clubs = Club.objects.filter(coachs=coach).order_by("-pk")
                elif active == 'Admin':
                    clubs = Club.objects.all().order_by("-pk")


            else:
                query = Q()
                if city:
                    query &= Q(communication__city__name__icontains=city)
                if name:
                    query &= Q(name__icontains=name)
                if clubMail:
                    query &= Q(clubMail__icontains=clubMail)
                if shortName:
                    query &= Q(shortName__icontains=shortName)
                if branch:
                    query &= Q(branch=branch)
                if kisi:
                    query &= Q(clubUser=kisi)
                if active == 'Kulüp Yetkilisi':
                    clubuser = SportClubUser.objects.get(user=user)
                    clubs = Club.objects.filter(clubUser=clubuser).filter(query)

                elif active == 'Yonetim' or active == 'Admin':
                    clubs = Club.objects.filter(query)

    return render(request, '_HavaSpor/Kulup/clubs.html',
                  {'clubs': clubs, 'ClupsSearchForm': ClupsSearchForm, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name, })


@login_required
def add_club(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    club_form = ClubForm()
    communication_form = CommunicationForm()
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    if request.method == 'POST':

        club_form = ClubForm(request.POST, request.FILES or None)
        communication_form = CommunicationForm(request.POST, request.FILES)

        if club_form.is_valid():
            clubsave = Club(name=club_form.cleaned_data['name'],
                            shortName=club_form.cleaned_data['shortName'],
                            foundingDate=club_form.cleaned_data['foundingDate'],
                            logo=club_form.cleaned_data['logo'],
                            clubMail=club_form.cleaned_data['clubMail'],
                            isFormal=club_form.cleaned_data['isFormal'],
                            petition=club_form.cleaned_data['petition'],


                            )

            communication = communication_form.save(commit=False)
            communication.save()
            clubsave.communication = communication
            clubsave.save()
            for branch in club_form.cleaned_data['branch']:
                clubsave.branch.add(branch)


            log = str(club_form.cleaned_data['name']) + " Klup eklendi"
            log = general_methods.logwrite(request, request.user, log)

            messages.success(request, 'Kulüp Başarıyla Kayıt Edilmiştir.')

            return redirect('sbs:return_clubs')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, '_HavaSpor/Kulup/add-club.html',
                  {'club_form': club_form, 'communication_form': communication_form ,'urls': urls, 'current_url': current_url,
                   'url_name': url_name,})


@login_required
def clubUpdate(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    club = Club.objects.get(uuid=uuid)

    athletes = Athlete.objects.filter(club=club)


    try:
        com_id = club.communication.pk
        communication = Communication.objects.get(id=com_id)
        communication_form = CommunicationForm(request.POST or None, instance=communication)
    except:
        communication_form = CommunicationForm(request.POST or None)

    club_form = ClubForm(request.POST or None, request.FILES or None, instance=club)
    clubPersons = club.clubUser.all()
    clubCoachs = club.coachs.all()
    if request.method == 'POST':
        if club_form.is_valid():
            club=club_form.save()

            if not club.communication:
                communication = communication_form.save(commit=False)
                communication.save()
                club.communication = communication
                club.save()


            else:
                communication_form.save()

            log = str(club) + " Kulüp güncellendi"
            log = general_methods.logwrite(request, request.user, log)


            messages.success(request, 'Başarıyla Güncellendi')
            return redirect('sbs:return_clubs')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, '_HavaSpor/Kulup/updateClub.html',
                  {'club_form': club_form, 'communication_form': communication_form, 'clubPersons': clubPersons,
                   'athletes': athletes,
                   'club': club, 'clubCoachs': clubCoachs})
