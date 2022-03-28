import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import resolve
from unicode_tr import unicode_tr
from zeep import Client

from sbs.Forms.havaspor.ClubForm import ClubForm
from sbs.Forms.havaspor.ClubUserForm import ClubUserForm
from sbs.Forms.havaspor.ClupUserSearchForm import ClubSearchForm
from sbs.Forms.havaspor.CommunicationForm import CommunicationForm
from sbs.Forms.havaspor.PersonForm import PersonForm
from sbs.Forms.havaspor.RefereeUserForm import RefereeUserForm
from sbs.Forms.havaspor.TransClubForm import TransClubForm
from sbs.Forms.havaspor.TransCommunicationForm import TransCommunicationForm
from sbs.Forms.havaspor.UserForm import UserForm
from sbs.models import Club, SportClubUser, Coach, Communication, Person
from sbs.models.ekabis.Permission import Permission
from sbs.models.tvfbf.License import License
from sbs.models.tvfbf.ClubRole import ClubRole
from sbs.models.tvfbf.Athlete import Athlete
from sbs.models.tvfbf.PreRegistration import PreRegistration
from sbs.models.tvfbf.ReferenceCoach import ReferenceCoach
from sbs.models.tvfbf.ReferenceReferee import ReferenceReferee
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
    clubs = Club.objects.filter(infoStatus=1).filter(isDeleted=False)
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
                    clubs = Club.objects.filter(clubUser=clubuser).filter(isDeleted=False).order_by("-pk")
                elif active == 'Antrenör':
                    coach = Coach.objects.get(user=user)
                    clubs = Club.objects.filter(coachs=coach).filter(isDeleted=False).order_by("-pk")
                elif active == 'Admin':
                    clubs = Club.objects.filter(isDeleted=False).order_by("-pk")


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
                    clubs = Club.objects.filter(clubUser=clubuser).filter(isDeleted=False).filter(query)

                elif active == 'Yonetim' or active == 'Admin':
                    clubs = Club.objects.filter(query).filter(isDeleted=False)

    return render(request, 'TVGFBF/Kulup/clubs.html',
                  {'clubs': clubs, 'ClupsSearchForm': ClupsSearchForm, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name, })


@login_required
def add_club(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    club_form = TransClubForm()
    manager_communication_form = CommunicationForm()
    manager_person_form = PersonForm()
    user_form = RefereeUserForm()
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    if request.method == 'POST':

        club_form = TransClubForm(request.POST or None, request.FILES or None)
        manager_communication_form = CommunicationForm(request.POST or None, request.FILES)
        manager_person_form = PersonForm(request.POST or None, request.FILES or None)
        user_form = RefereeUserForm(request.POST or None, request.FILES)

        try:
            with transaction.atomic():
                if club_form.is_valid() and user_form.is_valid() and manager_person_form.is_valid() and manager_communication_form.is_valid():
                    clubsave = Club()
                    clubsave.name = club_form.cleaned_data['name']
                    clubsave.foundingDate = club_form.cleaned_data['foundingDate'].strftime("%d/%m/%Y")
                    clubsave.derbis = club_form.cleaned_data['derbis']
                    clubsave.clubMail = club_form.cleaned_data['clubMail']
                    clubsave.save()
                    communication = Communication()
                    communication.city = City.objects.get(name=request.POST.get("clubIl"))
                    communication.phoneNumber = request.POST.get("clubPhone")
                    communication.address = request.POST.get("clubAdres")
                    communication.town = request.POST.get("clubIlce")
                    communication.fax = request.POST.get("clubFax")
                    communication.save()
                    clubsave.communication = communication
                    clubsave.save()

                    managerUser = User()
                    managerUser.username = user_form.cleaned_data['email']

                    managerUser.first_name = unicode_tr(user_form.cleaned_data['first_name']).upper()
                    managerUser.last_name = unicode_tr(user_form.cleaned_data['last_name']).upper()
                    managerUser.email = user_form.cleaned_data['email']

                    group = Group.objects.get(name='Kulüp Yetkilisi')
                    password = User.objects.make_random_password()
                    managerUser.set_password(password)
                    managerUser.is_active = True
                    managerUser.save()

                    managerUser.groups.add(group)
                    managerUser.save()

                    person = manager_person_form.save(commit=False)
                    managerCommunication = manager_communication_form.save(commit=False)
                    person.user = managerUser
                    person.save()
                    managerCommunication.save()

                    manager = SportClubUser()
                    manager.communication = managerCommunication
                    manager.person = person
                    manager.user = managerUser
                    role = ClubRole.objects.get(name='BAŞKAN')
                    manager.role = role
                    manager.save()

                    clubsave.clubUser.add(manager)
                    clubsave.save()

                    log = str(club_form.cleaned_data['name']) + " Klup eklendi"
                    log = general_methods.logwrite(request, request.user, log)

                    messages.success(request, 'Kulüp ve Kulüp Başkanı Başarıyla Kayıt Edilmiştir.')

                    return redirect('sbs:return_clubs')

                else:

                    messages.warning(request, 'Alanları Kontrol Ediniz')
                return render(request, 'TVGFBF/Kulup/add-club.html',
                              {'club_form': club_form, 'urls': urls, 'current_url': current_url,
                               'url_name': url_name, 'manager_communication_form': manager_communication_form,
                               'manager_person_form': manager_person_form, 'user_form': user_form, })


        except Exception as e:
            messages.warning(request, 'HATA !! ' + ' ' + str(e))
            return redirect('sbs:add_club')



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
            club = club_form.save()

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

    return render(request, 'TVGFBF/Kulup/updateClub.html',
                  {'club_form': club_form, 'communication_form': communication_form, 'clubPersons': clubPersons,
                   'athletes': athletes,
                   'club': club, 'clubCoachs': clubCoachs})


@login_required
def club_delete(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():

                obj = Club.objects.get(uuid=request.POST['uuid'])
                # if License.objects.filter(sportsClub=obj):
                #     return JsonResponse(
                #         {'status': 'Fail', 'messages': 'Kulüp silinemez!! Kulübe ait lisans bulunmaktadır'})
                # else:
                obj.delete()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Bir Hata ile Karşılaşıldı'})
    except Club.DoesNotExist:
        return JsonResponse({'status': 'Fail', 'msg': 'Kulüp Bununamadı'})


@login_required
def deleteCoachFromClub(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Coach.objects.get(uuid=request.POST['coach_uuid'])
            club = Club.objects.get(uuid=request.POST['club_uuid'])

            club.coachs.remove(obj)

            log = str(club) + " Antrenör kulüpten çıkarıldı"
            log = general_methods.logwrite(request, request.user, log)
            club.save()

            return JsonResponse({'status': 'Success', 'messages': 'delete successfully'})
        except ClubRole.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

@login_required
def deleteClubUserFromClub(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = SportClubUser.objects.get(uuid=request.POST['user_uuid'])
            club = Club.objects.get(uuid=request.POST['club_uuid'])

            club.clubUser.remove(obj)

            log = str(club) + " Kulüp üyesi çıkarıldı"
            log = general_methods.logwrite(request, request.user, log)

            club.save()

            return JsonResponse({'status': 'Success', 'messages': 'delete successfully'})
        except ClubRole.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})



@login_required
def detailClubUser(request):
    # perm = general_methods.control_access(request)
    #
    # if not perm:
    #     logout(request)
    #     return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']

                obj = SportClubUser.objects.get(uuid=uuid)
                clubUser = {}
                clubUser['name'] = obj.person.user.get_full_name()
                clubUser['tc'] = obj.person.tc
                clubUser['email'] = obj.person.user.email
                clubUser['phone'] = obj.communication.phoneNumber
                clubUser['image'] = obj.person.profileImage.url
                role = ''

                if obj.role:
                    role=obj.role.name
                clubUser['role'] = role
                club=''
                if Club.objects.filter(clubUser=obj):
                    club=Club.objects.get(clubUser=obj).name
                clubUser['club']=club

                return JsonResponse({'status': 'Success',
                                         'results': clubUser,
                                         })
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except Coach.DoesNotExist:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def return_add_club_person(request,uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user_form = UserForm()
    person_form = PersonForm()
    communication_form = CommunicationForm()
    sportClubUser_form = ClubUserForm()
    club=Club.objects.get(uuid=uuid)
    if request.method == 'POST':

        user_form = UserForm(request.POST)
        person_form = PersonForm(request.POST, request.FILES)
        communication_form = CommunicationForm(request.POST, request.FILES)
        sportClubUser_form =ClubUserForm(request.POST)

        mail = request.POST.get('email')

        # if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
        #         email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
        #     email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
        #     email=mail):
        #     messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
        #     return render(request, 'kulup/kulup-uyesi-ekle.html',
        #                   {'user_form': user_form, 'person_form': person_form, 'communication_form': communication_form,
        #                    'sportClubUser_form': sportClubUser_form,
        #                    })

        # tc = request.POST.get('tc')
        # if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
        #         tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
        #     tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
        #     messages.warning(request, 'Tc kimlik numarasi sisteme kayıtlıdır. ')
        #     return render(request, 'kulup/kulup-uyesi-ekle.html',
        #                   {'user_form': user_form, 'person_form': person_form, 'communication_form': communication_form,
        #                    'sportClubUser_form': sportClubUser_form,
        #                    })

        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        year = request.POST.get('birthDate')
        year = year.split('/')

        # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
        # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
        #     messages.warning(request, 'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
        #     return render(request, 'kulup/kulup-uyesi-ekle.html',
        #                   {'user_form': user_form, 'person_form': person_form, 'communication_form': communication_form,
        #                    'sportClubUser_form': sportClubUser_form,
        #                    })

        if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid() and sportClubUser_form.is_valid():
            user = User()
            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            group = Group.objects.get(name='Kulüp Yetkilisi')
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            user.groups.add(group)
            user.save()

            person = person_form.save(commit=False)
            communication = communication_form.save(commit=False)
            person.save()
            communication.save()

            club_person = SportClubUser(
                user=user, person=person, communication=communication,
                role=sportClubUser_form.cleaned_data['role'],

            )

            club_person.save()
            club.clubUser.add(club_person)

            # subject, from_email, to = 'Halter - Kulüp Üye Bilgi Sistemi Kullanıcı Giriş Bilgileri', 'no-reply@twf.gov.tr', user.email
            # text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
            # html_content = '<p> <strong>Site adresi: </strong> <a href="https://sbs.halter.gov.tr:9443/"></a>https://sbs.halter.gov.tr</p>'
            # html_content = html_content + '<p><strong>Kullanıcı Adı:  </strong>' + user.username + '</p>'
            # html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()

            log = str(user.get_full_name()) + " Kulüp üyesi eklendi"
            log = general_methods.logwrite(request, request.user, log)

            messages.success(request, 'Kulüp Üyesi Başarıyla Kayıt Edilmiştir.')

            return redirect('sbs:update_club' ,club.uuid)

        else:

            for x in user_form.errors.as_data():
                messages.warning(request, user_form.errors[x][0])

    return render(request, 'TVGFBF/Kulup/add_clubuser.html',
                  {'user_form': user_form, 'person_form': person_form, 'communication_form': communication_form,
                   'sportClubUser_form': sportClubUser_form,
                   })



@login_required
def choose_coach_clup(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    club= Club.objects.get(uuid=uuid)

    coachsPk = []
    for coach in club.coachs.all():
        coachsPk.append(coach.pk)
    coaches = Coach.objects.exclude(id__in=coachsPk)

    # license.athlete_set.first

    if request.method == 'POST':
        coach = request.POST.getlist('selected_options')
        if coach:
            for coa in coach:
                club.coachs.add(Coach.objects.get(pk=coa))
                club.save()

            log = str(club) + " Kulüp antrenör eklendi"
            log = general_methods.logwrite(request, request.user, log)

        return redirect('sbs:update_club', club.uuid)
    return render(request, 'TVGFBF/Kulup/chosee-coach.html', {'coaches': coaches,'club':club})
