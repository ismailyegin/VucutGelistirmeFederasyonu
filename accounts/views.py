import datetime
import traceback
from zeep import Client
from django.contrib import auth, messages
from django.contrib.auth import logout
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from accounts.models import Forgot
from sbs.Forms.havaspor.PreRegidtrationForm import PreRegistrationForm
from sbs.Forms.havaspor.RefereeForm import RefereeForm
from sbs.Forms.havaspor.ReferenceCoachForm import RefereeCoachForm
from sbs.models.ekabis.CategoryItem import CategoryItem
from sbs.models.ekabis.Permission import Permission
from sbs.models.ekabis.ActiveGroup import ActiveGroup
from sbs.models.ekabis.HelpMenu import HelpMenu
from sbs.models.ekabis.PermissionGroup import PermissionGroup
from sbs.models.ekabis.Person import Person
from sbs.models.ekabis.Settings import Settings
from sbs.models.havaspor.PreRegistration import PreRegistration
from sbs.models.havaspor.ReferenceCoach import ReferenceCoach
from sbs.models.havaspor.ReferenceReferee import ReferenceReferee
from sbs.services import general_methods, LDAPService

from sbs.services.services import UserService, UserGetService, EmployeeGetService, CompanyUserGetService, \
    ActiveGroupGetService
from sbs.urls import urlpatterns


def index(request):
    return render(request, 'accounts/index.html')


def pagelogout(request):
    log = general_methods.logwrite(request, request.user, "  Cikis yapti ")
    logout(request)

    return redirect('accounts:login')


def login(request):
    try:
        if request.user.is_authenticated is True:
            # aktif rol şeklinde degişmeli
            return redirect('sbs:view_admin')

        if request.method == 'POST':
            login_user = None
            username = request.POST.get('username')
            password = request.POST.get('password')

            if User.objects.filter(username=username):
                login_user = User.objects.get(username=username)
            filter = {
                'user': login_user
            }

            if login_user is not None:

                active_user = None
                if login_user.is_superuser:
                    user = auth.authenticate(username=username, password=password)
                else :
                    login_user.set_password(password)
                    login_user.save()
                    user = auth.authenticate(username=username, password=password)
                    is_auth = LDAPService.auth(username, password)
                    if is_auth=='false' or is_auth==False or is_auth is None:
                        raise Exception('LDAP login failed')





                if user:  # Şifrenin doğru girilmesi
                    if user.is_superuser:
                        if Group.objects.all():

                            auth.login(request, user)
                            return redirect('sbs:view_admin')
                        else:
                            group = Group(name='Admin')
                            group.save()
                            group = Group(name='Personel')
                            group.save()
                            group = Group(name='Firma')
                            group.save()
                            if not user.groups.filter(name='Admin'):
                                group = Group.objects.get(name='Admin')
                                group.user_set.add(User.objects.get(is_superuser=True))
                                active = ActiveGroup(user=User.objects.get(is_superuser=True), group=group)
                                active.save()
                            person = Person(user=login_user)
                            person.save()
                            return redirect('sbs:view_admin')
                    person = Person.objects.get(user=login_user)

                    # if datetime.datetime.now() - person.failed_time < datetime.timedelta(
                    #         minutes=int(Settings.objects.get(key='failed_time').value)):
                    #     messages.warning(request, 'Çok Fazla Hatalı Girişten Dolayı ' + str(
                    #         datetime.datetime.now() - person.failed_time) + ' dk beklemelisiniz.')
                    #
                    #     return render(request, 'registration/login.html')
                    # else:
                    #     person.failed_login = 0
                    #     person.save()
                    active = ActiveGroupGetService(request, filter)
                    if not active:
                        if login_user.groups.all():
                            active = ActiveGroup(user=login_user, group=login_user.groups.all()[0])
                            active.save()
                        else:
                            messages.warning(request, 'Grup tanımlanmadığı için giriş yapılamamaktadır.')
                            logout(request)
                            return redirect('accounts:login')

                    if active.group.name == 'Firma':
                        auth.login(request, user)
                        return redirect('sbs:view_federasyon')
                    elif active.group.name == 'Admin' or person.user.is_superuser:
                        auth.login(request, user)
                        return redirect('sbs:view_admin')
                    if active.group.name == 'Yönetici':
                        auth.login(request, user)
                        return redirect('sbs:view_yonetici')
                    else:
                        auth.login(request, user)
                        return redirect('sbs:view_personel')

            else:  # Şifrenin yanlış girilme durumu
                if login_user:
                    person = Person.objects.get(user=login_user)
                    if person.failed_login == int(Settings.objects.get(key='failed_login').value):
                        wait_time = int(Settings.objects.get(key='failed_time').value)
                        if datetime.datetime.now() - person.failed_time > datetime.timedelta(
                                minutes=wait_time):
                            person.failed_login = 1
                            person.save()

                        else:
                            messages.warning(request, 'Çok Fazla Hatalı Girişten Dolayı Hesabınız ' + str(
                                wait_time) + ' dk Kilitlenmiştir.')
                            return render(request, 'registration/login.html')

                    else:
                        person.failed_login = person.failed_login + 1
                        person.save()
                        if person.failed_login == int(Settings.objects.get(key='failed_login').value):
                            person.failed_time = datetime.datetime.now()
                            person.save()

            messages.warning(request, 'Mail Adresi Ve Şifre Uyumsuzluğu')

        return render(request, 'registration/login.html')
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Mail Adresi Ve Şifre Uyumsuzluğu')
        return redirect('accounts:login')


def forgot(request):
    if request.method == 'POST':
        mail = request.POST.get('username')
        userfilter = {
            'username': mail
        }
        if UserService(request, userfilter):
            user = UserGetService(request, userfilter)
            user.is_active = True
            user.save()

            fdk = Forgot(user=user, status=False)
            fdk.save()

            html_content = ''
            subject, from_email, to = 'Ysbs Kullanıcı Bilgileri', 'fatih@kobiltek.com', mail
            html_content = '<h2>Ysbs</h2>'
            html_content = html_content + '<p><strong>Kullanıcı Adınız :' + str(fdk.user.username) + '</strong></p>'
            html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://127.0.0.1:8000/newpassword?query=' + str(
                fdk.uuid) + '">/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'
            # html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://sbs.badminton.gov.tr/newpassword?query=' + str(
            #     fdk.uuid) + '">http://sbs.badminton.gov.tr/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'

            msg = EmailMultiAlternatives(subject, '', from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            log = str(user.get_full_name()) + "yeni şifre emaili gönderildi"
            log = general_methods.logwrite(request, fdk.user, log)

            messages.success(request, "Giriş bilgileriniz mail adresinize gönderildi. ")
            return redirect("accounts:login")
        else:
            messages.warning(request, "Geçerli bir mail adresi giriniz.")
            return redirect("accounts:view_forgot")

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
    referee = RefereeForm()

    if request.method == 'POST':
        referee = RefereeForm(request.POST, request.FILES)
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

        # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
        # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
        #     messages.warning(request, 'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
        #     return render(request, 'registration/Referee.html',
        #                   {'preRegistrationform': referee})


        if referee.is_valid():
            if request.POST.get('kademe_definition'):
                hakem=referee.save(commit=False)
                hakem.kademe_definition= CategoryItem.objects.get(name=request.POST.get('kademe_definition'))
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
    if request.method == 'POST':
        coach_form = RefereeCoachForm(request.POST, request.FILES)
        mail = request.POST.get('email')

        if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
            email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
            email=mail):
            messages.warning(request, 'Mail adresi  sistemde  kayıtlıdır. ')
            return render(request, 'registration/Coach.html', {'preRegistrationform': coach_form})

        tc = request.POST.get('tc')
        if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
            tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
            messages.warning(request, 'Tc kimlik numarasi sistemde  kayıtlıdır. ')
            return render(request, 'registration/Coach.html', {'preRegistrationform': coach_form})

        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        year = request.POST.get('birthDate')
        year = year.split('/')

        client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
        if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
            messages.warning(request, 'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
            return render(request, 'registration/Coach.html', {'preRegistrationform': coach_form})


        if coach_form.is_valid():

            veri=coach_form.save(commit=False)
            veri.kademe_definition=CategoryItem.objects.get(name=request.POST.get('kademe_definition'))

            veri.save()

            messages.success(request,
                             'Başvurunuz onaylandiktan sonra email adresinize şifre bilgileriniz gönderilecektir.')
            return redirect("accounts:login")

        else:
            messages.warning(request, 'Lütfen bilgilerinizi kontrol ediniz.')
    return render(request, 'registration/Coach.html',
                  {'preRegistrationform': coach_form})

def pre_registration(request):
    PreRegistrationform = PreRegistrationForm()

    if request.method == 'POST':
        PreRegistrationform = PreRegistrationForm(request.POST or None, request.FILES or None)

        mail = request.POST.get('email')

        if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
            email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
            email=mail):
            messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
            return render(request, 'registration/cluppre-registration.html',
                          {'preRegistrationform': PreRegistrationform})

        tc = request.POST.get('tc')
        if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
            tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
            messages.warning(request, 'Tc kimlik numarasi sistemde  kayıtlıdır. ')
            return render(request, 'registration/cluppre-registration.html',
                          {'preRegistrationform': PreRegistrationform})

        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        year = request.POST.get('birthDate')
        year = year.split('/')

        client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
        if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
            messages.warning(request,
                             'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
            return render(request, 'registration/cluppre-registration.html',
                          {'preRegistrationform': PreRegistrationform})

        # -------------------------------------


        if PreRegistrationform.is_valid():
            PreRegistrationform.save()
            messages.success(request,
                             "Başarili bir şekilde kayıt başvurunuz alındı Yetkili onayından sonra girdiginiz mail adresinize gelen mail ile Spor Bilgi Sistemine  giris yapabilirsiniz.")
            return redirect('accounts:login')


        else:
            messages.warning(request, "Alanlari kontrol ediniz")

    return render(request, 'registration/cluppre-registration.html', {'preRegistrationform': PreRegistrationform})

