# -*- coding: utf-8 -*-

import datetime
import traceback

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.staticfiles import finders
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
            elif active.group.name == 'Antrenör':
                return redirect('sbs:antrenor')
            elif active.group.name == 'Admin' or login_user.is_superuser:
                return redirect('sbs:view_admin')
            elif active.group.name == 'Yönetim':
                return redirect('sbs:federasyon')
            elif active.group.name == 'Kulüp Yetkilisi':
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
            elif active.group.name == 'Antrenör':
                return redirect('sbs:antrenor')
            elif active.group.name == 'Admin' or user.is_superuser:
                return redirect('sbs:view_admin')
            elif active.group.name == 'Yönetim':
                return redirect('sbs:federasyon')
            elif active.group.name == 'Kulüp Yetkilisi':
                return redirect('sbs:kulup-uyesi')

        else:
            # eski kullanici olma ihtimaline göre sisteme girme yöntemi

            try:
                user = Club.objects.get(username=request.POST.get('username'),
                                        password=request.POST.get('password'))

                if user is not None:
                    if user.isRegister == False or user.isRegister is None:
                        return redirect('accounts:newlogin', user.pk)

            except:
                print()

            messages.warning(request, 'Mail Adresi Ve Şifre Uyumsuzluğu')
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
                # zaman kontrolüde yapilacak
                gelen.status = True
                messages.success(request, 'Şifre Başarıyla Güncellenmiştir.')

                return redirect('accounts:login')


            else:

                messages.warning(request, 'Alanları Kontrol Ediniz')
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
        if active.is_active == True:

            if UserService(request, userfilter):
                user = UserGetService(request, userfilter)
                user.is_active = True
                user.save()

                fdk = Forgot(user=user, status=False)
                fdk.save()

                html_content = ''
                subject, from_email, to = 'TVGFBF Bilgi Sistemi Kullanıcı Bilgileri', EMAIL_HOST_USER, mail
                html_content = '<h2>Türkiye Vücut Geliştirme, Fitness ve Bilek Güreşi Federasyonu</h2>'
                html_content = html_content + '<p><strong>Kullanıcı Adınız :' + str(fdk.user.username) + '</strong></p>'
                html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="https://sbs.tvgfbf.gov.tr/newpassword?query=' + str(
                     fdk.uuid) + '">href="https://sbs.tvgfbf.gov.tr/newpassword?query=' + str(fdk.uuid) + '</p></a>'
                #html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="https://sbs.tvgfbf.gov.tr/newpassword?query=' + str(
                #    fdk.uuid) + '">https://sbs.tvgfbf.gov.tr/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'

                msg = EmailMultiAlternatives(subject, '', from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                log = str(user.get_full_name()) + "yeni şifre emaili gönderildi"
                log = general_methods.logwrite(request, fdk.user, log)

                return redirect("accounts:redirect_password_update")
            else:
                messages.warning(request, "Geçerli bir mail adresi giriniz.")
                return redirect("accounts:view_forgot")
        else:
            return redirect("accounts:redirect_active_user")
    return render(request, 'registration/forgot-password.html')


def show_urls(request):
    for entry in urlpatterns:
        perm = Permission(codename=entry.name, codeurl=entry.pattern.regex.pattern, name=entry.name)
        if not (Permission.objects.filter(codename=entry.name)):
            perm.save()

    # bütün yetkiler verildi
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
    # Bütün url ler için yardım metni oluşturuldu.
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

    if request.method == 'POST':
        referee = PreRefereeForm(request.POST, request.FILES)
        mail = request.POST.get('email')
        if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
            email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
            email=mail):
            messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
            return render(request, 'registration/Referee.html', {'preRegistrationform': referee})

        tc = request.POST.get('tc')
        if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
            tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
            messages.warning(request, 'Tc kimlik numarasi sistemde kayıtlıdır. ')
            return render(request, 'registration/Referee.html',
                          {'preRegistrationform': referee})

        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        year = request.POST.get('birthDate')
        year = year.split('/')

        client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
        if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
            messages.warning(request, 'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
            return render(request, 'registration/Referee.html',
                          {'preRegistrationform': referee})

        if referee.is_valid():
            if request.POST.get('kademe_definition'):
                hakem = referee.save(commit=False)
                hakem.kademe_definition = CategoryItem.objects.get(name=request.POST.get('kademe_definition'))
                hakem.save()

                messages.success(request,
                                 'Başvurunuz onaylandiktan sonra email adresinize şifre bilgileriniz gönderilecektir.')
                return redirect("accounts:login")
            else:
                messages.warning(request, 'Lütfen bilgilerinizi kontrol ediniz. Kademe bilgisi giriniz:')

        else:
            messages.warning(request, 'Lütfen bilgilerinizi kontrol ediniz. ')
    return render(request, 'registration/Referee.html',
                  {'preRegistrationform': referee})


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
    try:

        if request.method == 'POST':
            if request.POST.get('submitFormControl') == 'registerForm':
                coach_form = RefereeCoachForm(request.POST, request.FILES)
                mail = request.POST.get('email')

                if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(
                        status=ReferenceCoach.DENIED).filter(
                        email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
                    email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
                    email=mail):
                    messages.warning(request, 'Mail adresi  sistemde  kayıtlıdır. ')
                    return render(request, 'registration/Coach.html',
                                  {'preRegistrationform': coach_form, 'clubs': clubs, 'countries': countries,
                                   'cities': cities, 'grades': grades, })

                tc = request.POST.get('tc')
                if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                        tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
                    tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
                    messages.warning(request, 'Tc kimlik numarasi sistemde  kayıtlıdır. ')
                    return render(request, 'registration/Coach.html',
                                  {'preRegistrationform': coach_form, 'clubs': clubs, 'countries': countries,
                                   'cities': cities, 'grades': grades, })

                name = request.POST.get('first_name')
                surname = request.POST.get('last_name')
                year = request.POST.get('birthDate')
                year = year.split('/')

                client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
                if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
                    messages.warning(request,
                                     'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
                    return render(request, 'registration/Coach.html',
                                  {'preRegistrationform': coach_form, 'clubs': clubs, 'countries': countries,
                                   'cities': cities, 'grades': grades, })

                if coach_form.is_valid():

                    veri = coach_form.save(commit=False)
                    veri.kademe_definition = CategoryItem.objects.get(name=request.POST.get('kademe_definition'))
                    veri.country = coach_form.cleaned_data['country']

                    clubDersbis = request.POST.get('club', None)
                    if clubDersbis:
                        coachClub = Club.objects.get(derbis=clubDersbis)
                        veri.club = coachClub

                    veri.save()

                    return redirect("accounts:redirect_register")

                else:
                    messages.warning(request, 'Lütfen bilgilerinizi kontrol ediniz.')
            else:
                currentCoach = ReferenceCoach.objects.get(tc=request.POST.get('tcUpdate'))
                if request.FILES.get('profileImageUpdate'):
                    currentCoach.profileImage = request.FILES.get('profileImageUpdate')
                currentCoach.first_name = request.POST.get('firstNameUpdate')
                currentCoach.last_name = request.POST.get('lastNameUpdate')
                currentCoach.birthplace = request.POST.get('birthPlaceUpdate')
                currentCoach.iban = request.POST.get('ibanUpdate')
                currentCoach.tc = request.POST.get('tcUpdate')
                birthDate = request.POST.get('birthDateUpdate')
                currentCoach.birthDate = datetime.datetime.strptime(birthDate, "%d/%m/%Y").strftime("%Y-%m-%d")
                currentCoach.gender = request.POST.get('genderUpdate', None)
                if Club.objects.filter(name=request.POST.get('clubUpdate')):
                    currentCoach.club = Club.objects.get(name=request.POST.get('clubUpdate'))
                elif request.POST.get('clubUpdate') == '':
                    currentCoach.club = None
                if request.FILES.get('belgeUpdate'):
                    currentCoach.belge = request.FILES.get('belgeUpdate')
                currentCoach.email = request.POST.get('emailUpdate')
                currentCoach.phoneNumber = request.POST.get('phoneNumberUpdate')
                currentCoach.phoneNumber2 = request.POST.get('phoneNumber2Update')
                if Country.objects.filter(name=request.POST.get('countryUpdate')):
                    currentCoach.country = Country.objects.get(name=request.POST.get('countryUpdate'))
                if City.objects.filter(name=request.POST.get('cityUpdate')):
                    currentCoach.city = City.objects.get(name=request.POST.get('cityUpdate'))
                currentCoach.address = request.POST.get('addressUpdate')
                if CategoryItem.objects.filter(name=request.POST.get('gradeUpdate')):
                    currentCoach.kademe_definition = CategoryItem.objects.get(name=request.POST.get('gradeUpdate'))
                if request.FILES.get('kademeBelgeUpdate'):
                    currentCoach.kademe_belge = request.FILES.get('kademeBelgeUpdate')
                if request.FILES.get('sgkUpdate'):
                    currentCoach.sgk = request.FILES.get('sgkUpdate')
                if request.FILES.get('dekontUpdate'):
                    currentCoach.dekont = request.FILES.get('dekontUpdate')
                currentCoach.status=currentCoach.WAITED
                currentCoach.save()

                messages.success(request, 'Başvurunuz başarıyla güncellenmiştir.')

                return redirect("accounts:redirect_register")

        return render(request, 'registration/Coach.html',
                      {'preRegistrationform': coach_form, 'clubs': clubs, 'taahhut': x, 'countries': countries,
                       'cities': cities, 'grades': grades, })
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
        #     messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
        #     return render(request, 'registration/referenceRegisterClub.html',
        #                   {'preRegistrationform': PreRegistrationform})

        # tc = request.POST.get('tc')
        # if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
        #         tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
        #     tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
        #     messages.warning(request, 'Tc kimlik numarasi sistemde  kayıtlıdır. ')
        #     return render(request, 'registration/referenceRegisterClub.html',
        #                   {'preRegistrationform': PreRegistrationform})

        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        year = request.POST.get('birthDate')
        year = year.split('/')

        # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
        # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
        #     messages.warning(request,
        #                      'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
        #     return render(request,'registration/referenceRegisterClub.html',
        #                   {'preRegistrationform': PreRegistrationform})

        # -------------------------------------

        if preRegistrationform.is_valid():
            preRegistrationform.save()
            messages.success(request,
                             "Başarili bir şekilde kayıt başvurunuz alındı Yetkili onayından sonra girdiginiz mail adresinize gelen mail ile Spor Bilgi Sistemine  giris yapabilirsiniz.")
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
                             "Başarili bir şekilde kayıt başvurunuz alındı.")
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
                             "Başarili bir şekilde kayıt başvurunuz alındı.")
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
                             "Başarili bir şekilde kayıt başvurunuz alındı.")
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