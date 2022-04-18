import traceback
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.messages import get_messages
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.urls import resolve
from django.utils.safestring import mark_safe



import xml.etree.ElementTree as ET
from urllib.request import urlopen
import ssl

from accounts.models import Forgot
from sbs.models.ekabis.Logs import Logs
from sbs.models.ekabis.ActiveGroup import ActiveGroup
from sbs.models.ekabis.HelpMenu import HelpMenu
from sbs.models.ekabis.Menu import Menu
from sbs.models.ekabis.NotificationUser import NotificationUser
from sbs.models.ekabis.Permission import Permission
from sbs.models.ekabis.PermissionGroup import PermissionGroup
from sbs.services.services import MenuService, PermissionGroupService, ActiveGroupService, ActiveGroupGetService, \
    UserService, UserGetService


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def logwrite(request, user, log):
    try:
        logs = Logs(user=user, subject=log, ip=get_client_ip(request))
        logs.save()

        # Txt dosyaya kayıt
        # f = open("log.txt", "a")
        # log = get_client_ip(request) + "    [" + datetime.today().strftime('%d-%m-%Y %H:%M') + "] " + str(
        #     user) + " " + log + " \n "
        # f.write(log)
        # f.close()

    except Exception as e:
        f = open("log.txt", "a")
        log = "[" + datetime.today().strftime('%d-%m-%Y %H:%M') + "]  lag kaydetme hata   \n "
        f.write(log)
        f.close()

    return log


def getMenu(request):
    menus = MenuService(request, None)
    active = controlGroup(request)
    activefilter = {
        'group__name': active,
        'is_active': True

    }
    permGrup = PermissionGroupService(request, activefilter)
    menu = []
    activ_urls = None
    url = request.resolver_match.url_name
    if Permission.objects.filter(codename=request.resolver_match.url_name):
        login_url = Permission.objects.get(codename=request.resolver_match.url_name)
        if login_url:
            if login_url.parent:
                url = login_url.parent.codename
    for item in menus:
        if item.is_parent == False:
            if item.url:
                for tk in permGrup:
                    if tk.permissions.codename == item.url.split(":")[1]:
                        if url == item.url.split(":")[1]:
                            activ_urls = item
                        menu.append(item.pk)
                        menu.append(item.parent.pk)

                        pass

    menus = Menu.objects.filter(id__in=menu).distinct()
    return {'menus': menus, 'activ_url': activ_urls}


def control_access(request):
    is_exist = False
    groupfilter = {
        'user': request.user
    }
    if ActiveGroupService(request, groupfilter):
        aktifgroup = ActiveGroupGetService(request, groupfilter).group
        for perm in PermissionGroup.objects.filter(group=aktifgroup, is_active=True):
            if request.resolver_match.url_name == perm.permissions.codename:
                print('Okay')
                is_exist = True
    else:
        if request.user.groups.all():
            aktifgroup = ActiveGroup(
                user=request.user,
                group=request.user.groups.all()[0]
            )
            aktifgroup.save()
        else:
            logout(request)
            return is_exist

    if request.user.groups.filter(name="Admin"):
        is_exist = True
    return is_exist


def aktif(request):
    userfilter = {
        'pk': request.user.pk
    }
    if UserService(request, userfilter):
        activfilter = {
            'user': request.user
        }

        aktifgroup = None

        if not (ActiveGroupService(request, activfilter)):
            if request.user.groups.all():
                aktifgroup = ActiveGroup(user=request.user, group=request.user.groups.all()[0])
                aktifgroup.save()
                aktif = aktifgroup.group.name
            else:
                logout(request)
                return redirect('accounts:login')

        else:
            activfilter = {
                'user': request.user
            }
            aktifgroup = ActiveGroupGetService(request, activfilter)
            # aktifgroup = ActiveGroupService(request, activfilter)[0]
            aktif = aktifgroup.group.name
        perm = []

        groupfilter = {
            'group__id': aktifgroup.group.pk,
            'is_active': True
        }
        permission = PermissionGroupService(request, groupfilter)
        for item in permission:
            perm.append(item.permissions.codename)

        group = request.user.groups.all()
        return {'aktif': aktif,
                'group': group,
                'perm': perm,
                }
    else:
        return {}


def controlGroup(request):
    userfilter = {
        'pk': request.user.pk
    }
    if UserService(request, userfilter):
        activfilter = {
            'user': request.user
        }
        if not (ActiveGroupService(request, activfilter)):
            if request.user.groups.all():
                aktive = ActiveGroup(user=request.user, group=request.user.groups.all().last())
                aktive.save()
                active = request.user.groups.all().last().name
            else:
                logout(request)
                return redirect('accounts:login')

        else:
            activfilter = {
                'user': request.user
            }
            active = ActiveGroupGetService(request, activfilter)
            active = active.group.name
        return active

    else:
        return {}


def getProfileImage(request):
    if (request.user.id):
        userfilter = {
            'person__user': request.user
        }

        if request.user.groups.filter(name='Admin').exists():
            person = dict()
            person['profileImage'] = "profile/logo.png"
        else:
            person = None
        return {'person': person}
    return {}


def get_notification(request):
    notifications = None
    date = None
    notification_count = 0
    if request.user.id:
        user = request.user
        notifications = NotificationUser.objects.filter(is_read=False, user=user).order_by('-creationDate')[:10]
        notification_count = NotificationUser.objects.filter(is_read=False, user=user).order_by('-creationDate').count()
        date = datetime.now().date()
    return {'notifications': notifications, 'date': date, 'notification_count': notification_count}


def get_error_messages(form):
    if form:
        error_messages = []
        for key in form.errors:
            for field in form.fields:
                if key == field:
                    entry = {'key': field, 'value': form.errors[key][0]}
                    error_messages.append(entry)
        return error_messages
    return {}


def get_help_text(request):
    current_url_name = resolve(request.path_info).url_name
    help_text = ''
    help_url = ''
    texts = HelpMenu.objects.filter(isDeleted=False)
    for text in texts:
        if text.url.codename == current_url_name:
            help_text = text.text
            help_url = text.uuid
            break
    return {'text': help_text
        , 'help_url': help_url}


def do_something_with_the_message(message):
    pass


def yeka_control(request, yeka):
    storage = get_messages(request)
    for message in storage:
        if message.level_tag == 'warning':
            return None
    message = []
    yekafilter = {
        'yeka': yeka
    }
    url = None
    # Çalısma sırasına göre  sıraladık ona göre if döngülerinin sonucunda deger alacak

    if not (yeka.business):
        messages.add_message(request, messages.WARNING, 'İş Blokları Bilgileri Eksik.')
        url = "view_yekabusinessBlog"

    # if not (YekaCompanyService(request,yekafilter)):
    #     messages.add_message(request, messages.WARNING, 'Firma Bilgileri Eksik.')
    #     url="view_yeka_company"

    # if not (YekaPersonService(request, yekafilter)):
    #     messages.add_message(request, messages.WARNING, 'Personel Bilgileri Eksik.')
    #     url = "view_yeka_personel"
    if url:
        return url
    else:
        return None


def competition_control(request, competiton):
    storage = get_messages(request)
    for message in storage:
        if message.level_tag == 'warning':
            return None
    message = []

    url = None
    # Çalısma sırasına göre  sıraladık ona göre if döngülerinin sonucunda deger alacak

    if not (competiton.business):
        messages.add_message(request, messages.WARNING, 'İş Blokları Bilgileri Eksik.')
        url = "view_competitionbusinessblog"

    # if not (YekaCompanyService(request,yekafilter)):
    #     messages.add_message(request, messages.WARNING, 'Firma Bilgileri Eksik.')
    #     url="view_yeka_company"

    # if not (YekaCompetitionPersonService(request, {'competition': competiton})):
    #     messages.add_message(request, messages.WARNING, 'Personel Bilgileri Eksik.')
    #     url = "view_yekacompetition_personel"
    if url:
        return url
    else:
        return None


def sendmail(request, pk):
    try:
        userfilter = {
            'pk': pk
        }
        user = UserGetService(request, userfilter)
        fdk = Forgot(user=user, status=False)
        fdk.save()

        subject, from_email, to = 'Yekabis Kullanıcı Bilgileri', 'fatih@kobiltek.com', user.email
        html_content = '<h2>YEKABİS</h2>'
        html_content = html_content + '<p><strong>Kullanıcı Adınız :' + str(fdk.user.username) + '</strong></p>'
        html_content = html_content + '<p> <strong>Aktivasyon adresi:</strong> <a href="http://127.0.0.1:8000/newpassword?query=' + str(
            fdk.uuid) + '">/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'

        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        log = str(user.get_full_name()) + "yeni şifre emaili gönderildi"
        log = logwrite(request, fdk.user, log)

        return True
    except Exception as e:
        traceback.print_exc()



def log(request):
    try:
        log = Logs()
        log.user = request.user
        log.ip = get_client_ip(request)
        url = Permission.objects.get(codename=request.resolver_match.url_name).name
        log.subject = url
        return log
    except Exception as e:
        traceback.print_exc()


def log_model(request, pre, next):
    try:
        log = Logs()
        log.user = request.user
        log.ip = get_client_ip(request)
        url = Permission.objects.get(codename=request.resolver_match.url_name).name
        log.subject = url
        log.previousData = pre
        log.nextData = next
        log.save()
        return log
    except Exception as e:
        traceback.print_exc()




def kur():
    # kur bilgilerinin alındıgı alan
    url = "https://www.tcmb.gov.tr/kurlar/today.xml"
    gcontext = ssl.SSLContext()  # Only for gangstars
    info = urlopen(context=gcontext, url=url)
    tree = ET.parse(info)
    root = tree.getroot()
    son = {}
    data = []
    i = 0
    for kurlars in root.findall('Currency'):
        Kod = kurlars.get('Kod')
        Unit = kurlars.find('Unit').text  # <Unit>1</Unit>
        isim = kurlars.find('Isim').text  # <Isim>ABD DOLARI</Isim>
        CurrencyName = kurlars.find('CurrencyName').text  # <CurrencyName>US DOLLAR</CurrencyName>
        ForexBuying = kurlars.find('ForexBuying').text  # <ForexBuying>2.9587</ForexBuying>
        ForexSelling = kurlars.find('ForexSelling').text  # <ForexSelling>2.964</ForexSelling>
        BanknoteBuying = kurlars.find('BanknoteBuying').text  # <BanknoteBuying>2.9566</BanknoteBuying>
        BanknoteSelling = kurlars.find('BanknoteSelling').text  # <BanknoteSelling>2.9684</BanknoteSelling>
        CrossRateUSD = kurlars.find('CrossRateUSD').text  # <CrossRateUSD>1</CrossRateUSD>
        son = {
            "Kod": Kod,
            "isim": isim,
            "CurrencyName": CurrencyName,
            "Unit": Unit,
            "ForexBuying": ForexBuying,
            "ForexSelling": ForexSelling,
            "BanknoteBuying": BanknoteBuying,
            "BanknoteSelling": BanknoteSelling,
            "CrossRateUSD": CrossRateUSD
        }
        data.append(son)
    return data


# def ufe():
#     # üfe tüfe bilgilerinin alındıgı alan
#     data = []
#
#     url = "https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Istatistikler/Enflasyon+Verileri/Uretici+Fiyatlari"
#     response = requests.get(url)
#     html_icerigi = response.content
#     soup = BeautifulSoup(html_icerigi, "html.parser")
#     tr = soup.find_all("tr")
#     data = []
#     for td in tr:
#         if td.find_all("strong"):
#             print(td.text)
#             test = td.text.split('\n')
#         else:
#             print(td.text)
#             t = td.text.split('\n')
#             if len(t) == 7 and t:
#                 beka = {
#                     'date': t[1],
#                     'yiufe': t[2],
#                     'ufe': t[3],
#                     'yitufe': t[4],
#                     'tufe': t[5],
#                 }
#                 data.append(beka)
#     return data








def control_access_kulup(request):
    groups = request.user.groups.all()
    is_exist = False

    for group in groups:
        permissions = group.permissions.all()

        for perm in permissions:

            if request.resolver_match.url_name == perm.name:
                is_exist = True

        if group.name == "Admin" or group.name == "Hakem" or group.name == "Antrenör" or group.name == "Yonetim" or group.name == "Kulup Yetkilisi":
            is_exist = True

    return is_exist


def control_access_klup(request):
    current_user = request.user
    if current_user.groups.filter(name='Kulup Yetkilisi').exists():

        is_exist = True

    else:
        group = request.user.groups.all()[0]

        permissions = group.permissions.all()

        is_exist = False

        for perm in permissions:

            if request.resolver_match.url_name == perm.name:
                is_exist = True

        if group.name == "Admin" or group.name == "Kulüp Yetkilisi" or group.name == "Antrenör" or group.name == "Yonetim":
            is_exist = True

    return is_exist

def control_access_referee(request):
    group = request.user.groups.all()[0]

    permissions = group.permissions.all()

    is_exist = False

    for perm in permissions:

        if request.resolver_match.url_name == perm.name:
            is_exist = True

    if group.name == "Admin" or group.name == "Hakem" or group.name == "Yonetim":
        is_exist = True

    return is_exist
