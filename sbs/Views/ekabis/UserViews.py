import traceback

from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import resolve

from sbs.Forms.UserForm import UserForm
from sbs.Forms.UserSearchForm import UserSearchForm
from accounts.models import Forgot
from sbs.models import SportClubUser, Coach, Referee, Organizer
from sbs.models.ekabis.Permission import Permission
from sbs.models.tvfbf.Athlete import Athlete
from sbs.services import general_methods
from sbs.services.general_methods import get_error_messages
from sbs.services.services import UserService, GroupService, UserGetService, GroupGetService, GroupExcludeService, \
    last_urls

from django.contrib.auth.models import Group
from sbs.models.ekabis.HistoryGroup import HistoryGroup


@login_required
def return_users(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user_form = UserSearchForm()
    try:
        # urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        filter = {
                'is_active': True,
                'is_superuser':False
        }
        users = UserService(request, filter)[:10]

        return render(request, 'kullanici/kullanicilar.html',
                      {'users': users, 'user_form': user_form, 'current_url': current_url,
                           'url_name': url_name})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def update_user(request, pk):
    userfilter = {
        'pk': pk
    }
    user = UserGetService(request, userfilter)
    user_form = UserForm(request.POST or None, instance=user)
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':

                if user_form.is_valid():
                    user = user_form.save(request,commit=False)
                    user.username = user_form.cleaned_data['email']
                    user.first_name = user_form.cleaned_data['first_name']
                    user.last_name = user_form.cleaned_data['last_name']
                    user.email = user_form.cleaned_data['email']
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Kullanıcı Başarıyla Güncellendi')
                    return redirect('ekabis:view_user')
                else:
                    error_messages = get_error_messages(user_form)
                    return render(request, 'kullanici/kullanici-duzenle.html',
                                  {'user_form': user_form, 'error_messages': error_messages, 'urls': urls, 'current_url': current_url, 'url_name': url_name})

        return render(request, 'kullanici/kullanici-duzenle.html',
                      {'user_form': user_form, 'error_messages': '','urls': urls, 'current_url': current_url, 'url_name': url_name})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def active_user(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():

                userfilter = {
                    'pk': pk
                }

                obj = UserGetService(request, userfilter)
                if obj.is_active:
                    obj.is_active = False
                    obj.save()
                else:
                    obj.is_active = True
                    obj.save()
                print(obj.is_active)
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def send_information(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():

                userfilter = {
                    'uuid': uuid
                }

                user = UserGetService(request, userfilter)

                if not user.is_active:
                    return JsonResponse({'status': 'Fail', 'msg': 'Kullanıcıyı aktifleştirin.'})
                fdk = Forgot(user=user, status=False)
                fdk.save()
                html_content = ''
                subject, from_email, to = 'Yekabis Kullanıcı Bilgileri', 'fatih@kobiltek.com', user.email
                html_content = '<h2>Yekabis</h2>'
                html_content = html_content + '<p><strong>Kullanıcı Adınız :' + str(fdk.user.username) + '</strong></p>'
                # html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://127.0.0.1:8000/newpassword?query=' + str(
                #     fdk.uuid) + '">http://127.0.0.1:8000/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'
                html_content = html_content + '<p> <strong>Yeni şifre oluşturma linki:</strong> <a href="https://www.kobiltek.com:81/yekabis/sbs/newpassword?query=' + str(
                    fdk.uuid) + '">https://www.kobiltek.com:81/yekabis/sbs/profil-guncelle/?query=' + str(
                    fdk.uuid) + '</p></a>'
                msg = EmailMultiAlternatives(subject, '', from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                log = general_methods.logwrite(request, " Yeni giris maili gönderildi" + str(user))
                return JsonResponse({'status': 'Success', 'msg': 'Şifre başarıyla gönderildi'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def change_group_function(request, pk):
    perm = general_methods.control_access(request)

    # if not perm:
    #     logout(request)
    #     return redirect('accounts:login')
    userfilter = {
        'pk': pk
    }
    user = UserGetService(request, userfilter)
    user_group = Group.objects.filter(user=user)
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    if request.POST:
        list = request.POST.getlist('test')
        # eklenme durumu -

        if Coach.objects.filter(person__user=user):
            coachInfo = Coach.objects.get(person__user=user)
            communicationInfo = coachInfo.communication
            personInfo = coachInfo.person
        elif Referee.objects.filter(person__user=user):
            refereeInfo = Referee.objects.get(person__user=user)
            communicationInfo = refereeInfo.communication
            personInfo = refereeInfo.person
        elif SportClubUser.objects.filter(person__user=user):
            clubUserInfo = SportClubUser.objects.get(person__user=user)
            communicationInfo = clubUserInfo.communication
            personInfo = clubUserInfo.person
        elif Organizer.objects.filter(person__user=user):
            organizerInfo = Organizer.objects.get(person__user=user)
            communicationInfo = organizerInfo.communication
            personInfo = organizerInfo.person
        elif Athlete.objects.filter(person__user=user):
            athleteInfo = Athlete.objects.get(person__user=user)
            communicationInfo = athleteInfo.communication
            personInfo = athleteInfo.person
        else:
            messages.warning(request, 'Yeni Grup Kaydı İçin Kullanıcının İletişim ve Kişisel Bilgileri Bulunamadı.')
            return redirect('sbs:change_user_group', pk=user.pk)

        for item in list:
            if Group.objects.exclude(pk=item):
                groupfilter = {
                    'pk': item
                }
                group = GroupGetService(request, groupfilter)

                user.groups.add(group)
                user.save()
                if group.name == 'Antrenör':
                    if not Coach.objects.filter(person__user=user):
                        coach = Coach(communication=communicationInfo, person=personInfo)
                        coach.save()
                    else:
                        coach = Coach.objects.get(person__user=user)
                        coach.isDeleted = False
                        coach.save()
                elif group.name == 'Hakem':
                    if not Referee.objects.filter(person__user=user):
                        referee = Referee(communication=communicationInfo, person=personInfo)
                        referee.save()
                    else:
                        referee = Referee.objects.get(person__user=user)
                        referee.isDeleted = False
                        referee.save()
                elif group.name == 'Kulüp Yetkilisi':
                    if not SportClubUser.objects.filter(person__user=user):
                        clubUser = SportClubUser(communication=communicationInfo, person=personInfo)
                        clubUser.save()
                    else:
                        clubUser = SportClubUser.objects.get(person__user=user)
                        clubUser.isDeleted = False
                        clubUser.save()
                elif group.name == 'Organizatör':
                    if not Organizer.objects.filter(person__user=user):
                        organizer = Organizer(communication=communicationInfo, person=personInfo)
                        organizer.save()
                    else:
                        organizer = Organizer.objects.get(person__user=user)
                        organizer.isDeleted = False
                        organizer.save()
                elif group.name == 'Sporcu':
                    if not Athlete.objects.filter(person__user=user):
                        athlete = Athlete(communication=communicationInfo, person=personInfo)
                        athlete.save()
                    else:
                        athlete = Athlete.objects.get(person__user=user)
                        athlete.isDeleted = False
                        athlete.save()
                history = HistoryGroup(
                    user=user,
                    group=group,
                    is_active=True
                )
                history.save()

        # silme durumu
        for item in user_group:
            is_active = True
            for i in list:
                if i == str(item.pk):
                    is_active = False
            if is_active:
                if item.name == 'Antrenör':
                    coach = Coach.objects.get(person__user=user)
                    coach.isDeleted = True
                    coach.save()
                elif item.name == 'Hakem':
                    referee = Referee.objects.get(person__user=user)
                    referee.isDeleted = True
                    referee.save()
                elif item.name == 'Kulüp Yetkilisi':
                    clubUser = SportClubUser.objects.get(person__user=user)
                    clubUser.isDeleted = True
                    clubUser.save()
                elif item.name == 'Organizatör':
                    organizer = Organizer.objects.get(person__user=user)
                    organizer.isDeleted = True
                    organizer.save()
                elif item.name == 'Sporcu':
                    athlete = Athlete.objects.get(person__user=user)
                    athlete.isDeleted = True
                    athlete.save()
                user.groups.remove(item)
                user.save()
                history = HistoryGroup(
                    user=user,
                    group=group,
                    is_active=False
                )
                history.save()
    userfilter = {
        'user': user
    }
    user_group = GroupService(request, userfilter)
    user_none_group = GroupExcludeService(request, userfilter)

    return render(request, 'kullanici/kullniciGrupEkle.html',
                  {"user_none_group": user_none_group,
                   "user_group": user_group,
                   'user': user, 'urls': urls, 'current_url': current_url, 'url_name': url_name})
