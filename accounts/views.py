# -*- coding: utf-8 -*-

import datetime
import traceback

import unidecode
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.staticfiles import finders
from validate_email import validate_email
from django.db import transaction
from django.forms import forms
from django.http import JsonResponse
from numpy import unicode
from zeep import Client
from django.contrib import auth, messages
from django.contrib.auth import logout
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from accounts.models import Forgot
from oxiterp.settings.base import EMAIL_HOST_USER
from sbs.Forms.SportFacilityForm import SportFacilityForm
from sbs.Forms.havaspor.ReferenCoachApiForm import RefereeCoachApiForm
from sbs.Forms.havaspor.ReferenceAthleteForm import ReferenceAthleteForm
from sbs.Forms.havaspor.ReferenceCoachForm import RefereeCoachForm
from sbs.Forms.havaspor.PreRefereeForm import PreRefereeForm
from sbs.Forms.havaspor.PreRegidtrationForm import PreRegistrationForm
from sbs.Forms.havaspor.RefereeForm import RefereeForm
from sbs.Forms.havaspor.ReferenceCoachForm import RefereeCoachForm
from sbs.models import SportFacility, ReferenceSportFacility, ReferenceAthlete, Branch, Country, City
from sbs.models.tvfbf.Club import Club
from sbs.models.ekabis.CategoryItem import CategoryItem
from sbs.models.ekabis.Permission import Permission
from sbs.models.ekabis.ActiveGroup import ActiveGroup
from sbs.models.ekabis.HelpMenu import HelpMenu
from sbs.models.ekabis.PermissionGroup import PermissionGroup
from sbs.models.ekabis.Person import Person
from sbs.models.ekabis.Settings import Settings
from sbs.models.tvfbf.PreRegistration import PreRegistration
from sbs.models.tvfbf.ReferenceCoach import ReferenceCoach
from sbs.models.tvfbf.ReferenceReferee import ReferenceReferee
from sbs.services import general_methods

from sbs.services.services import UserService, UserGetService, ActiveGroupGetService
from sbs.urls import urlpatterns


def index(request):
    return render(request, 'accounts/index.html')


def pagelogout(request):
    log = general_methods.logwrite(request, request.user, "  Cikis yapti ")
    logout(request)

    return redirect('accounts:login')


def login(request):
    if request.user.is_authenticated is True:
        if User.objects.filter(username=request.user.username):
            login_user = User.objects.get(username=request.user.username)
            filter = {
                'user': login_user
            }
            active = ActiveGroupGetService(request, filter)

            if active.group.name == 'Hakem':
                return redirect('sbs:hakem')
            elif active.group.name == 'Antren??r':
                return redirect('sbs:antrenor')
            elif active.group.name == 'Admin' or login_user.is_superuser:
                return redirect('sbs:view_admin')
            elif active.group.name == 'Y??netim':
                return redirect('sbs:federasyon')
            elif active.group.name == 'Kul??p Yetkilisi':
                return redirect('sbs:kulup-uyesi')

    if request.method == 'POST':
        login_user = None
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = None
        if User.objects.filter(username=username):
            user = User.objects.get(username=username)

        if user is not None:

            auth.login(request, user)

            print(general_methods.get_client_ip(request))

            log = general_methods.logwrite(request, request.user, " Giris yapti")

            filter = {
                'user': user
            }
            active = ActiveGroupGetService(request, filter)
            if not active:
                if request.user.groups.all():
                    active = ActiveGroup(user=request.user, group=request.user.groups.all()[0])
                    active.save()

            if active.group.name == 'Hakem':
                return redirect('sbs:hakem')
            elif active.group.name == 'Antren??r':
                return redirect('sbs:antrenor')
            elif active.group.name == 'Admin' or user.is_superuser:
                return redirect('sbs:view_admin')
            elif active.group.name == 'Y??netim':
                return redirect('sbs:federasyon')
            elif active.group.name == 'Kul??p Yetkilisi':
                return redirect('sbs:kulup-uyesi')

        else:
            # eski kullanici olma ihtimaline g??re sisteme girme y??ntemi

            try:
                user = Club.objects.get(username=request.POST.get('username'),
                                        password=request.POST.get('password'))

                if user is not None:
                    if user.isRegister == False or user.isRegister is None:
                        return redirect('accounts:newlogin', user.pk)

            except:
                print()

            messages.warning(request, 'Mail Adresi Ve ??ifre Uyumsuzlu??u')
            return render(request, 'registration/login.html')

    return render(request, 'registration/login.html')


def updateUrlProfile(request):
    if request.method == 'GET':
        try:
            data = request.GET.get('query')
            gelen = Forgot.objects.get(uuid=data)
            user = gelen.user
            password_form = SetPasswordForm(user)

            gelen.status = True
            gelen.save()
            return render(request, 'registration/newPassword.html',
                          {'password_form': password_form})

        except:
            return redirect('accounts:login')

    if request.method == 'POST':
        try:
            gelen = Forgot.objects.get(uuid=request.GET.get('query'))
            password_form = SetPasswordForm(gelen.user, request.POST)
            user = gelen.user
            if password_form.is_valid():
                user.set_password(password_form.cleaned_data['new_password1'])
                user.save()
                # zaman kontrol??de yapilacak
                gelen.status = True
                return redirect("accounts:redirect_newpassword")

            else:

                messages.warning(request, 'Alanlar?? Kontrol Ediniz')
                return render(request, 'registration/newPassword.html',
                              {'password_form': password_form})
        except:
            return redirect('accounts:login')

    return render(request, 'accounts/index.html')


def forgot(request):
    if request.method == 'POST':
        mail = request.POST.get('username')
        userfilter = {
            'username': mail
        }
        active = UserGetService(request, userfilter)
        if active:
            if active.is_active == True:

                if UserService(request, userfilter):
                    user = UserGetService(request, userfilter)
                    user.is_active = True
                    user.save()

                    fdk = Forgot(user=user, status=False)
                    fdk.save()

                    html_content = ''
                    subject, from_email, to = 'TVGFBF Bilgi Sistemi Kullan??c?? Bilgileri', EMAIL_HOST_USER, mail
                    html_content = '<h2>T??rkiye V??cut Geli??tirme, Fitness ve Bilek G??re??i Federasyonu</h2>'
                    html_content = html_content + '<p><strong>Kullan??c?? Ad??n??z :' + str(
                        fdk.user.username) + '</strong></p>'
                    html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="https://sbs.tvgfbf.gov.tr/newpassword?query=' + str(
                        fdk.uuid) + '">href="https://sbs.tvgfbf.gov.tr/newpassword?query=' + str(fdk.uuid) + '</p></a>'
                    # html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="https://sbs.tvgfbf.gov.tr/newpassword?query=' + str(
                    #    fdk.uuid) + '">https://sbs.tvgfbf.gov.tr/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'

                    msg = EmailMultiAlternatives(subject, '', from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    log = str(user.get_full_name()) + "yeni ??ifre emaili g??nderildi"
                    log = general_methods.logwrite(request, fdk.user, log)

                    return redirect("accounts:redirect_password_update")
                else:
                    messages.warning(request, "Ge??erli bir mail adresi giriniz.")
                    return redirect("accounts:forgot")
            else:
                return redirect("accounts:redirect_active_user")
        else:
            messages.warning(request, "Ge??erli bir mail adresi giriniz.")
            return redirect("accounts:forgot")
    return render(request, 'registration/forgot-password.html')


def send_new_password(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                pk = request.POST.get('pk')
                userfilter = {
                    'pk': pk
                }
                active = UserGetService(request, userfilter)
                if active.is_active == True:

                    if UserService(request, userfilter):
                        user = UserGetService(request, userfilter)
                        password = User.objects.make_random_password()
                        user.set_password(password)
                        user.is_active = True
                        user.save()

                        subject, from_email, to = 'TVGFBF Bilgi Sistemi Kullan??c?? Giri?? Bilgileri', EMAIL_HOST_USER, user.email
                        html_content = '<h2>T??rkiye V??cut Geli??tirme, Fitness ve Bilek G??re??i Federasyonu</h2>'
                        html_content = html_content + '<p><strong>Kullan??c?? Ad??n??z :' + str(
                            user.username) + '</strong></p>'
                        html_content = html_content + '<p><strong>??ifreniz :' + str(password) + '</strong></p>'
                        html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="https://sbs.tvgfbf.gov.tr">sbs.tvgfbf.gov.tr</a></p>'

                        msg = EmailMultiAlternatives(subject, '', from_email, [to])
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()

                        log = str(user.get_full_name()) + "yeni ??ifre emaili g??nderildi"
                        log = general_methods.logwrite(request, user, log)
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
    except ReferenceReferee.DoesNotExist:
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


def show_urls(request):
    for entry in urlpatterns:
        perm = Permission(codename=entry.name, codeurl=entry.pattern.regex.pattern, name=entry.name)
        if not (Permission.objects.filter(codename=entry.name)):
            perm.save()

    # b??t??n yetkiler verildi
    groups = Group.objects.all()
    for group in groups:
        for item in Permission.objects.all():
            if not (PermissionGroup.objects.filter(group=group, permissions=item)):
                if group.name == 'Admin':
                    perm = PermissionGroup(group=group,
                                           permissions=item,
                                           is_active=True)
                else:
                    perm = PermissionGroup(group=group,
                                           permissions=item,
                                           is_active=False)

                perm.save()
    # B??t??n url ler i??in yard??m metni olu??turuldu.
    for item in Permission.objects.all():
        if not HelpMenu.objects.filter(url=item):
            help = HelpMenu(
                text=" ",
                url=item
            )
            help.save()
    return redirect('accounts:login')


def handler404(request, *args, **argv):
    return redirect('accounts:handler404template')


def handler500(request, *args, **argv):
    return redirect('accounts:handler500template')


def handle400Template(request):
    return render(request, '404.html')


def handle500Template(request):
    return render(request, '500.html')


def handler404(request, *args, **argv):
    return redirect('accounts:404')


def handler500(request, *args, **argv):
    return redirect('accounts:500')


def handle400Template(request):
    return render(request, 'Ayar/404.html')


def handle500Template(request):
    return render(request, 'Ayar/500.html')


def referenceReferee(request):
    logout(request)
    referee = PreRefereeForm()
    referee.fields['sgk'].required = True
    referee.fields['referee_file'].required = True
    referee.fields['grade_referee_contract'].required = True
    countries = Country.objects.all()
    cities = City.objects.all()
    grades = CategoryItem.objects.filter(forWhichClazz="REFEREE_GRADE", isDeleted=0).order_by('order')

    if request.method == 'POST':
        if request.POST.get('submitFormControl') == 'registerForm':
            referee = PreRefereeForm(request.POST, request.FILES)
            mail = request.POST.get('email')
            if User.objects.filter(email=mail) or ReferenceCoach.objects.filter(
                    email=mail) or ReferenceReferee.objects.filter(email=mail) or PreRegistration.objects.filter(
                email=mail):
                messages.warning(request, 'Mail adresi ba??ka bir kullanici taraf??ndan kullanilmaktadir.')
                return render(request, 'registration/Referee.html',
                              {'preRegistrationform': referee, 'countries': countries,
                               'cities': cities, 'grades': grades, })

            tc = request.POST.get('tc')
            if Person.objects.filter(tc=tc) or ReferenceCoach.objects.filter(tc=tc) or ReferenceReferee.objects.filter(
                    tc=tc) or PreRegistration.objects.filter(tc=tc):
                messages.warning(request, 'Tc kimlik numarasi sistemde kay??tl??d??r. ')
                return render(request, 'registration/Referee.html',
                              {'preRegistrationform': referee, 'countries': countries,
                               'cities': cities, 'grades': grades, })

            name = request.POST.get('first_name')
            surname = request.POST.get('last_name')
            year = request.POST.get('birthDate')
            year = year.split('/')

            client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
            if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
                messages.warning(request, 'Tc kimlik numarasi ile isim  soyisim do??um y??l??  bilgileri uyu??mamaktad??r. ')
                return render(request, 'registration/Referee.html',
                              {'preRegistrationform': referee, 'countries': countries,
                               'cities': cities, 'grades': grades, })

            emailIsValid = validate_email(mail, verify=True)
            if emailIsValid == False:
                messages.warning(request, 'L??tfen ge??erli bir email adresi giriniz.')
                return render(request, 'registration/Referee.html',
                              {'preRegistrationform': referee, 'countries': countries,
                               'cities': cities, 'grades': grades, })

            if referee.is_valid():
                hakem = referee.save(commit=False)

                hakem.country = Country.objects.get(name=request.POST.get('country'))
                hakem.kademe_definition = CategoryItem.objects.get(name=request.POST.get('kademe_definition'))
                hakem.gradeBranch = Branch.objects.get(title=request.POST.get('branch'))
                hakem.save()

                messages.success(request,
                                 'Ba??vurunuz onaylandiktan sonra email adresinize ??ifre bilgileriniz g??nderilecektir.')
                return redirect("accounts:redirect_register")

            else:
                messages.warning(request, 'L??tfen bilgilerinizi kontrol ediniz. ')
        else:
            currentReferee = ReferenceReferee.objects.get(tc=request.POST.get('tcUpdate'))
            mail = request.POST.get('emailUpdate')
            if User.objects.filter(email=mail) or ReferenceCoach.objects.filter(
                    email=mail) or ReferenceReferee.objects.exclude(uuid=currentReferee.uuid).filter(
                email=mail) or PreRegistration.objects.filter(email=mail):
                messages.warning(request, 'Mail adresi ba??ka bir kullanici taraf??ndan kullanilmaktadir.')
                return render(request, 'registration/Referee.html',
                              {'preRegistrationform': referee, 'countries': countries,
                               'cities': cities, 'grades': grades, })

            tc = request.POST.get('tcUpdate')
            if Person.objects.filter(tc=tc) or ReferenceCoach.objects.filter(tc=tc) or ReferenceReferee.objects.exclude(
                    uuid=currentReferee.uuid).filter(tc=tc) or PreRegistration.objects.filter(tc=tc):
                messages.warning(request, 'Tc kimlik numarasi sistemde kay??tl??d??r. ')
                return render(request, 'registration/Referee.html',
                              {'preRegistrationform': referee, 'countries': countries,
                               'cities': cities, 'grades': grades, })

            name = request.POST.get('firstNameUpdate')
            surname = request.POST.get('lastNameUpdate')
            year = request.POST.get('birthDateUpdate')
            year = year.split('/')

            client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
            if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
                messages.warning(request, 'Tc kimlik numarasi ile isim  soyisim do??um y??l??  bilgileri uyu??mamaktad??r. ')
                return render(request, 'registration/Referee.html',
                              {'preRegistrationform': referee, 'countries': countries,
                               'cities': cities, 'grades': grades, })

            if request.FILES.get('profileImageUpdate'):
                currentReferee.profileImage = request.FILES.get('profileImageUpdate')
            currentReferee.first_name = request.POST.get('firstNameUpdate')
            currentReferee.last_name = request.POST.get('lastNameUpdate')
            currentReferee.birthplace = request.POST.get('birthPlaceUpdate')
            currentReferee.iban = request.POST.get('ibanUpdate')
            currentReferee.tc = request.POST.get('tcUpdate')
            birthDate = request.POST.get('birthDateUpdate')
            currentReferee.birthDate = datetime.datetime.strptime(birthDate, "%d/%m/%Y").strftime("%Y-%m-%d")
            currentReferee.gender = request.POST.get('genderUpdate', None)
            if request.FILES.get('belgeUpdate'):
                currentReferee.referee_file = request.FILES.get('belgeUpdate')
            currentReferee.email = request.POST.get('emailUpdate')
            currentReferee.phoneNumber = request.POST.get('phoneNumberUpdate')
            currentReferee.phoneNumber2 = request.POST.get('phoneNumber2Update')
            if Country.objects.filter(name=request.POST.get('countryUpdate')):
                currentReferee.country = Country.objects.get(name=request.POST.get('countryUpdate'))
            if City.objects.filter(name=request.POST.get('cityUpdate')):
                currentReferee.city = City.objects.get(name=request.POST.get('cityUpdate'))
            currentReferee.address = request.POST.get('addressUpdate')
            if CategoryItem.objects.filter(name=request.POST.get('gradeUpdate')):
                currentReferee.kademe_definition = CategoryItem.objects.get(name=request.POST.get('gradeUpdate'))
            if request.FILES.get('kademeBelgeUpdate'):
                currentReferee.grade_referee_contract = request.FILES.get('kademeBelgeUpdate')
            gradeDate = request.POST.get('gradeDateUpdate')
            currentReferee.gradeDate = datetime.datetime.strptime(gradeDate, "%d/%m/%Y").strftime("%Y-%m-%d")
            currentReferee.gradeNo = request.POST.get('gradeNoUpdate')
            if request.FILES.get('sgkUpdate'):
                currentReferee.sgk = request.FILES.get('sgkUpdate')
            currentReferee.save()

            messages.success(request, 'Ba??vurunuz ba??ar??yla g??ncellenmi??tir.')

            return redirect("accounts:redirect_register")
    return render(request, 'registration/Referee.html',
                  {'preRegistrationform': referee, 'countries': countries,
                   'cities': cities, 'grades': grades, })


def referenceCoach(request):
    logout(request)
    coach_form = RefereeCoachForm()
    coach_form.fields['sgk'].required = True
    coach_form.fields['dekont'].required = True
    coach_form.fields['kademe_belge'].required = True
    x = finders.find('images/taahhut.pdf')
    clubs = Club.objects.all().exclude(derbis__isnull=True)
    countries = Country.objects.all()
    cities = City.objects.all()
    grades = CategoryItem.objects.filter(forWhichClazz="COACH_GRADE", isDeleted=0).order_by('order')
    branchs = Branch.objects.filter(isDeleted=0)
    try:
        with transaction.atomic():
            if request.method == 'POST':
                if request.POST.get('submitFormControl') == 'registerForm':
                    coach_form = RefereeCoachForm(request.POST, request.FILES)
                    mail = request.POST.get('email')

                    if User.objects.filter(email=mail) or ReferenceCoach.objects.filter(
                            email=mail) or ReferenceReferee.objects.filter(
                        email=mail) or PreRegistration.objects.filter(
                        email=mail):
                        messages.warning(request, 'Mail adresi  sistemde  kay??tl??d??r. ')
                        return render(request, 'registration/Coach.html',
                                      {'preRegistrationform': coach_form, 'clubs': clubs, 'countries': countries,
                                       'cities': cities, 'grades': grades, 'branchs': branchs, })

                    tc = request.POST.get('tc')
                    if Person.objects.filter(tc=tc) or ReferenceCoach.objects.filter(
                            tc=tc) or ReferenceReferee.objects.filter(tc=tc) or PreRegistration.objects.filter(tc=tc):
                        messages.warning(request, 'Tc kimlik numarasi sistemde  kay??tl??d??r. ')
                        return render(request, 'registration/Coach.html',
                                      {'preRegistrationform': coach_form, 'clubs': clubs, 'countries': countries,
                                       'cities': cities, 'grades': grades, 'branchs': branchs, })

                    name = request.POST.get('first_name')
                    surname = request.POST.get('last_name')
                    year = request.POST.get('birthDate')
                    year = year.split('/')

                    client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
                    if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
                        messages.warning(request,
                                         'Tc kimlik numarasi ile isim  soyisim dogum y??l??  bilgileri uyu??mamaktad??r. ')
                        return render(request, 'registration/Coach.html',
                                      {'preRegistrationform': coach_form, 'clubs': clubs, 'countries': countries,
                                       'cities': cities, 'grades': grades, 'branchs': branchs, })

                    emailIsValid = validate_email(mail, verify=True)
                    if emailIsValid == False:
                        messages.warning(request, 'L??tfen ge??erli bir email adresi giriniz.')
                        return render(request, 'registration/Coach.html',
                                      {'preRegistrationform': coach_form, 'clubs': clubs, 'countries': countries,
                                       'cities': cities, 'grades': grades, 'branchs': branchs, })
                    if coach_form.is_valid():

                        veri = coach_form.save(commit=False)
                        veri.country = coach_form.cleaned_data['country']

                        if request.POST.get('vucutGrade'):
                            veri.kademe_definition = CategoryItem.objects.get(uuid=request.POST.get('vucutGrade'))
                            veri.kademe_brans = Branch.objects.get(title='V??CUT GEL????T??RME VE F??TNESS')
                            if request.FILES.get('belgeVucut'):
                                veri.belge = request.FILES.get('belgeVucut')
                                veri.belge.name = unidecode.unidecode(request.FILES.get('belgeVucut').name)

                        if request.POST.get('bilekGrade'):
                            veri.kademe_definition2 = CategoryItem.objects.get(uuid=request.POST.get('bilekGrade'))
                            veri.kademe_brans2 = Branch.objects.get(title='B??LEK G??RE????')
                            if request.FILES.get('belgeBilek'):
                                veri.belge2 = request.FILES.get('belgeBilek')
                                veri.belge2.name = unidecode.unidecode(request.FILES.get('belgeBilek').name)

                        if request.FILES.get('vucutVizeFile'):
                            veri.vize_brans = Branch.objects.get(title='V??CUT GEL????T??RME VE F??TNESS')
                            veri.dekont = request.FILES.get('vucutVizeFile')
                            veri.dekont.name = unidecode.unidecode(request.FILES.get('vucutVizeFile').name)

                        if request.FILES.get('bilekVizeFile'):
                            veri.vize_brans2 = Branch.objects.get(title='B??LEK G??RE????')
                            veri.dekont2 = request.FILES.get('bilekVizeFile')
                            veri.dekont2.name = unidecode.unidecode(request.FILES.get('bilekVizeFile').name)

                        clubDersbis = request.POST.get('club', None)
                        if clubDersbis:
                            coachClub = Club.objects.get(derbis=clubDersbis)
                            veri.club = coachClub

                        veri.save()

                        return redirect("accounts:redirect_register")

                    else:
                        messages.warning(request, 'L??tfen bilgilerinizi kontrol ediniz.')
                else:
                    currentCoach = ReferenceCoach.objects.get(tc=request.POST.get('tcUpdate'))
                    mail = request.POST.get('emailUpdate')
                    if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(uuid=currentCoach.uuid).filter(
                            email=mail) or ReferenceReferee.objects.filter(
                        email=mail) or PreRegistration.objects.filter(email=mail):
                        messages.warning(request, 'Mail adresi ba??ka bir kullanici taraf??ndan kullanilmaktadir.')
                        return render(request, 'registration/Coach.html',
                                      {'preRegistrationform': coach_form, 'clubs': clubs, 'taahhut': x,
                                       'countries': countries, 'cities': cities, 'grades': grades,
                                       'branchs': branchs, })

                    tc = request.POST.get('tcUpdate')
                    if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(
                            uuid=currentCoach.uuid).filter(tc=tc) or ReferenceReferee.objects.filter(
                        tc=tc) or PreRegistration.objects.filter(tc=tc):
                        messages.warning(request, 'Tc kimlik numarasi sistemde kay??tl??d??r. ')
                        return render(request, 'registration/Coach.html',
                                      {'preRegistrationform': coach_form, 'clubs': clubs, 'taahhut': x,
                                       'countries': countries, 'cities': cities, 'grades': grades,
                                       'branchs': branchs, })

                    name = request.POST.get('firstNameUpdate')
                    surname = request.POST.get('lastNameUpdate')
                    year = request.POST.get('birthDateUpdate')
                    year = year.split('/')

                    client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
                    if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
                        messages.warning(request,
                                         'Tc kimlik numarasi ile isim  soyisim do??um y??l??  bilgileri uyu??mamaktad??r. ')
                        return render(request, 'registration/Coach.html',
                                      {'preRegistrationform': coach_form, 'clubs': clubs, 'taahhut': x,
                                       'countries': countries, 'cities': cities, 'grades': grades,
                                       'branchs': branchs, })
                    if request.FILES.get('profileImageUpdate'):
                        currentCoach.profileImage = request.FILES.get('profileImageUpdate')
                        currentCoach.profileImage.name = unidecode.unidecode(request.FILES.get('profileImageUpdate').name)
                    currentCoach.first_name = request.POST.get('firstNameUpdate')
                    currentCoach.last_name = request.POST.get('lastNameUpdate')
                    currentCoach.birthplace = request.POST.get('birthPlaceUpdate')
                    currentCoach.iban = request.POST.get('ibanUpdate')
                    currentCoach.workplace = request.POST.get('workplaceUpdate')
                    currentCoach.tc = request.POST.get('tcUpdate')
                    birthDate = request.POST.get('birthDateUpdate')
                    workplace = request.POST.get('workplaceUpdate')
                    currentCoach.birthDate = datetime.datetime.strptime(birthDate, "%d/%m/%Y").strftime("%Y-%m-%d")
                    currentCoach.gender = request.POST.get('genderUpdate', None)
                    if Club.objects.filter(name=request.POST.get('clubUpdate')):
                        currentCoach.club = Club.objects.get(name=request.POST.get('clubUpdate'))
                    elif request.POST.get('clubUpdate') == '':
                        currentCoach.club = None
                    currentCoach.email = request.POST.get('emailUpdate')
                    currentCoach.phoneNumber = request.POST.get('phoneNumberUpdate')
                    currentCoach.phoneNumber2 = request.POST.get('phoneNumber2Update')
                    currentCoach.workplace = workplace
                    if Country.objects.filter(name=request.POST.get('countryUpdate')):
                        currentCoach.country = Country.objects.get(name=request.POST.get('countryUpdate'))
                    if City.objects.filter(name=request.POST.get('cityUpdate')):
                        currentCoach.city = City.objects.get(name=request.POST.get('cityUpdate'))
                    currentCoach.address = request.POST.get('addressUpdate')
                    if request.FILES.get('kademeBelgeUpdate'):
                        currentCoach.kademe_belge = request.FILES.get('kademeBelgeUpdate')
                        currentCoach.kademe_belge.name = unidecode.unidecode(request.FILES.get('kademeBelgeUpdate').name)
                    if request.FILES.get('sgkUpdate'):
                        currentCoach.sgk = request.FILES.get('sgkUpdate')
                        currentCoach.sgk.name = unidecode.unidecode(request.FILES.get('sgkUpdate').name)

                    if request.POST.get('vucutKademeUpdate'):
                        if request.POST.get('gradeUpdateVucut'):
                            currentCoach.kademe_definition = CategoryItem.objects.get(
                                name=request.POST.get('gradeUpdateVucut'))
                        if request.POST.get('branchUpdateVucut'):
                            currentCoach.kademe_brans = Branch.objects.get(title=request.POST.get('branchUpdateVucut'))
                        if request.FILES.get('belgeUpdateVucut'):
                            currentCoach.belge = request.FILES.get('belgeUpdateVucut')
                            currentCoach.belge.name = unidecode.unidecode(request.FILES.get('belgeUpdateVucut').name)
                    else:
                        currentCoach.kademe_definition = None
                        currentCoach.kademe_brans = None
                        currentCoach.belge = None

                    if request.POST.get('bilekKademeUpdate'):
                        if request.POST.get('gradeUpdateBilek'):
                            currentCoach.kademe_definition2 = CategoryItem.objects.get(
                                name=request.POST.get('gradeUpdateBilek'))
                        if request.POST.get('branchUpdateBilek'):
                            currentCoach.kademe_brans2 = Branch.objects.get(title=request.POST.get('branchUpdateBilek'))
                        if request.FILES.get('belgeUpdateBilek'):
                            currentCoach.belge2 = request.FILES.get('belgeUpdateBilek')
                            currentCoach.belge2.name = unidecode.unidecode(request.FILES.get('belgeUpdateBilek').name)
                    else:
                        currentCoach.kademe_definition2 = None
                        currentCoach.kademe_brans2 = None
                        currentCoach.belge2 = None

                    if request.POST.get('vucutVizeUpdate'):
                        if request.POST.get('vucutBranchVizeUpdate'):
                            currentCoach.vize_brans = Branch.objects.get(
                                title=request.POST.get('vucutBranchVizeUpdate'))
                        if request.FILES.get('vucutVizeFileUpdate'):
                            currentCoach.dekont = request.FILES.get('vucutVizeFileUpdate')
                            currentCoach.dekont.name = unidecode.unidecode(request.FILES.get('vucutVizeFileUpdate').name)
                    else:
                        currentCoach.vize_brans = None
                        currentCoach.dekont = None

                    if request.POST.get('bilekVizeUpdate'):
                        if request.POST.get('bilekBranchVizeUpdate'):
                            currentCoach.vize_brans2 = Branch.objects.get(
                                title=request.POST.get('bilekBranchVizeUpdate'))
                        if request.FILES.get('bilekVizeFileUpdate'):
                            currentCoach.dekont2 = request.FILES.get('bilekVizeFileUpdate')
                            currentCoach.dekont2.name = unidecode.unidecode(request.FILES.get('bilekVizeFileUpdate').name)
                    else:
                        currentCoach.vize_brans2 = None
                        currentCoach.dekont2 = None

                    currentCoach.status = currentCoach.WAITED
                    currentCoach.save()

                    messages.success(request, 'Ba??vurunuz ba??ar??yla g??ncellenmi??tir.')

                    return redirect("accounts:redirect_register")

            return render(request, 'registration/Coach.html',
                          {'preRegistrationform': coach_form, 'clubs': clubs, 'taahhut': x, 'countries': countries,
                           'cities': cities, 'grades': grades, 'branchs': branchs, })
    except Exception as e:
        traceback.print_exc()
        return redirect("accounts:login")


def pre_registration(request):
    preRegistrationform = PreRegistrationForm()
    clubs = Club.objects.all()

    if request.method == 'POST':
        preRegistrationform = PreRegistrationForm(request.POST or None, request.FILES or None)

        # mail = request.POST.get('email')
        #
        # if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
        #         email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
        #     email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
        #     email=mail):
        #     messages.warning(request, 'Mail adresi ba??ka bir kullanici taraf??ndan kullanilmaktadir.')
        #     return render(request, 'registration/referenceRegisterClub.html',
        #                   {'preRegistrationform': PreRegistrationform})

        # tc = request.POST.get('tc')
        # if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
        #         tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
        #     tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
        #     messages.warning(request, 'Tc kimlik numarasi sistemde  kay??tl??d??r. ')
        #     return render(request, 'registration/referenceRegisterClub.html',
        #                   {'preRegistrationform': PreRegistrationform})

        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        year = request.POST.get('birthDate')
        year = year.split('/')

        # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
        # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
        #     messages.warning(request,
        #                      'Tc kimlik numarasi ile isim  soyisim dogum y??l??  bilgileri uyu??mamaktad??r. ')
        #     return render(request,'registration/referenceRegisterClub.html',
        #                   {'preRegistrationform': PreRegistrationform})

        # -------------------------------------

        if preRegistrationform.is_valid():
            preRegistrationform.save()
            messages.success(request,
                             "Ba??arili bir ??ekilde kay??t ba??vurunuz al??nd?? Yetkili onay??ndan sonra girdiginiz mail adresinize gelen mail ile Spor Bilgi Sistemine  giris yapabilirsiniz.")
            return redirect('accounts:login')


        else:
            messages.warning(request, "Alanlari kontrol ediniz")

    return render(request, 'registration/referenceRegisterClub.html',
                  {'preRegistrationform': preRegistrationform, 'clubs': clubs})


def pre_registration_facility(request):
    preRegistrationform = SportFacilityForm()
    if request.method == 'POST':
        preRegistrationform = SportFacilityForm(request.POST or None, request.FILES or None)

        if preRegistrationform.is_valid():
            pre_facility = ReferenceSportFacility(name=preRegistrationform.cleaned_data['name'],
                                                  derbis=preRegistrationform.cleaned_data['derbis'],
                                                  mersis=preRegistrationform.cleaned_data['mersis'],
                                                  registrationNumber=preRegistrationform.cleaned_data[
                                                      'registrationNumber'],
                                                  permitDate=preRegistrationform.cleaned_data['permitDate'],
                                                  coordinate=preRegistrationform.cleaned_data['coordinate'])
            pre_facility.save()
            messages.success(request,
                             "Ba??arili bir ??ekilde kay??t ba??vurunuz al??nd??.")
            return redirect('accounts:login')


        else:
            messages.warning(request, "Alanlari kontrol ediniz")

    return render(request, 'TVGFBF/SportFacility/referenceFacility.html',
                  {'preRegistrationform': preRegistrationform, })


def pre_registration_athelete(request):
    preRegistrationform = ReferenceAthleteForm()
    if request.method == 'POST':
        preRegistrationform = ReferenceAthleteForm(request.POST or None, request.FILES or None)

        if preRegistrationform.is_valid():
            veri = preRegistrationform.save(commit=False)
            veri.save()
            messages.success(request,
                             "Ba??arili bir ??ekilde kay??t ba??vurunuz al??nd??.")
            return redirect('accounts:login')


        else:
            messages.warning(request, "Alanlari kontrol ediniz")

    return render(request, 'registration/Athlete.html',
                  {'preRegistrationform': preRegistrationform, })


def pre_registration_coach_api(request):
    preRegistrationform = RefereeCoachApiForm()
    clubs = Club.objects.all()
    if request.method == 'POST':
        preRegistrationform = RefereeCoachApiForm(request.POST or None, request.FILES or None)

        if preRegistrationform.is_valid():
            veri = preRegistrationform.save(commit=False)

            clubDersbis = request.POST.get('club', None)
            if clubDersbis:
                coachClub = Club.objects.get(derbis=clubDersbis)
                veri.club = coachClub

            grade_count = request.POST['grade_count']
            kademe_derece = request.POST['kademeDerece' + grade_count]
            kademe_brans = request.POST['bransBilgi' + grade_count]
            kademe_durum = request.POST['vize' + grade_count]
            kademe_tarih = request.POST['duzenlenmeTarihi' + grade_count]
            dekont = request.FILES['dekont' + grade_count]
            sgkBelge = request.FILES['sgkBelge' + grade_count]
            kademeBelge = request.FILES['kademeBelge' + grade_count]

            veri.kademe_definition = CategoryItem.objects.get(name=kademe_derece)
            veri.kademe_branch = Branch.objects.get(title=kademe_brans)
            veri.kademe_startDate = datetime.datetime.strptime(kademe_tarih, '%Y-%m-%d')

            veri.sgk = sgkBelge
            veri.dekont = dekont
            veri.kademe_belge = kademeBelge

            veri.save()
            messages.success(request,
                             "Ba??arili bir ??ekilde kay??t ba??vurunuz al??nd??.")
            return redirect('accounts:login')


        else:
            messages.warning(request, "Alanlari kontrol ediniz")
            return redirect('accounts:pre_registration_coach_api')

    return render(request, 'registration/coachFromApi.html',
                  {'preRegistrationform': preRegistrationform, 'clubs': clubs})


def redirect_register(request):
    return render(request, 'registration/register_redirect_page.html')


def redirect_password_update(request):
    return render(request, 'registration/password-update-page.html')


def redirect_active_user(request):
    return render(request, 'registration/active_user.html')


def redirect_newpassword(request):
    return render(request, 'registration/redirect_newpassword.html')
