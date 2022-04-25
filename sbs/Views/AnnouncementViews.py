import datetime
import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import resolve

from sbs.Forms.havaspor.AnnouncementForm import AnnouncementForm
from sbs.models import Logs
from sbs.models.ekabis.NotificationUser import NotificationUser
from sbs.models.ekabis.Permission import Permission
from sbs.models.tvfbf.Announcement import Announcement
from sbs.models.tvfbf.AnnouncementUser import AnnouncementUser
from sbs.serializers.AnnouncementSerializers import AnnouncementSerializer
from sbs.serializers.NotificationUserSerializers import NotificationUserSerializer
from sbs.services import general_methods
from sbs.services.general_methods import get_client_ip
from sbs.services.services import last_urls


@login_required
def returnAnnouncement(request):
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        login_user = request.user

        if login_user.groups.filter(name='Admin'):
            announcements = Announcement.objects.all().order_by('-creationDate')
        else:
            announcements = AnnouncementUser.objects.filter(user=login_user).order_by('-creationDate')
        return render(request, 'TVGFBF/Announcement/announcements.html',
                      {'announcements': announcements, 'urls': urls, 'current_url': current_url,
                       'url_name': url_name.name})
    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('sbs:view_admin')


@login_required
def addAnnouncement(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    announcement_form = AnnouncementForm()

    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    if request.method == 'POST':
        announcement_form = AnnouncementForm(request.POST, request.FILES)

        if announcement_form.is_valid():
            announcement = Announcement()
            announcement.title = announcement_form.cleaned_data['title']
            announcement.text = request.POST.get('announcementText')
            announcement.startDate = announcement_form.cleaned_data['startDate']
            announcement.finishDate = announcement_form.cleaned_data['finishDate']
            announcement.save()
            for group in announcement_form.cleaned_data['group']:
                announcement.group.add(group)
            announcement.save()
            for user in User.objects.filter(groups__in=announcement_form.cleaned_data['group']):
                announcementUser = AnnouncementUser(
                    announcement=announcement, user=user
                )
                announcementUser.save()
            messages.success(request, 'Duyuru Başarıyla Kayıt Edilmiştir.')

            return redirect('sbs:announcements')

        else:

            for x in announcement_form.errors.as_data():
                messages.warning(request, announcement_form.errors[x][0])
    return render(request, 'TVGFBF/Announcement/add-announcement.html',
                  {'announcement_form': announcement_form, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name, })


@login_required
def updateAnnouncement(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    selectedAnnouncement = Announcement.objects.get(uuid=uuid)
    announcement_form = AnnouncementForm(request.POST or None, request.FILES or None, instance=selectedAnnouncement)

    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    if request.method == 'POST':
        announcement_form = AnnouncementForm(request.POST or None, request.FILES or None, instance=selectedAnnouncement)

        if announcement_form.is_valid():
            selectedAnnouncement.title = announcement_form.cleaned_data['title']
            selectedAnnouncement.text = request.POST.get('announcementText')
            selectedAnnouncement.startDate = announcement_form.cleaned_data['startDate']
            selectedAnnouncement.finishDate = announcement_form.cleaned_data['finishDate']
            selectedAnnouncement.modificationDate = datetime.datetime.now()

            for announcementGroup in selectedAnnouncement.group.all():
                if not announcementGroup in announcement_form.cleaned_data['group']:
                    selectedAnnouncement.group.remove(announcementGroup)
                    for announcementUser in AnnouncementUser.objects.filter(announcement=selectedAnnouncement).filter(
                            user__groups=announcementGroup):
                        announcementUser.delete()
            selectedAnnouncement.save()

            for group in announcement_form.cleaned_data['group']:
                if not group in selectedAnnouncement.group.all():
                    selectedAnnouncement.group.add(group)
                    for user in User.objects.filter(groups=group):
                        announcementUser = AnnouncementUser(
                            announcement=selectedAnnouncement, user=user
                        )
                        announcementUser.save()

            selectedAnnouncement.save()

            messages.success(request, 'Duyuru Başarıyla Güncellenmiştir.')

            return redirect('sbs:announcements')

        else:

            for x in announcement_form.errors.as_data():
                messages.warning(request, announcement_form.errors[x][0])
    return render(request, 'TVGFBF/Announcement/update-announcement.html',
                  {'announcement_form': announcement_form, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name, 'selectedAnnouncement': selectedAnnouncement, })


@login_required
def delete_announcement(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']

                announcement = Announcement.objects.get(uuid=uuid)
                announcementUsers = AnnouncementUser.objects.filter(announcement=announcement)

                data_as_json_pre = serializers.serialize('json', Announcement.objects.filter(uuid=uuid))

                for announcementUser in announcementUsers:
                    announcementUser.delete()

                announcement.delete()

                log = "Duyuru Silindi"
                logs = Logs(user=request.user, subject=log, ip=get_client_ip(request),
                            previousData=data_as_json_pre)
                logs.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


def getAnnouncement(request):
    try:

        if request.method == 'POST' and request.is_ajax():
            uuid = request.POST['uuid']
            announcement = Announcement.objects.filter(uuid=uuid)
            data = AnnouncementSerializer(announcement, many=True)

            if not request.user.groups.filter(name='Admin'):
                userAnnouncement = Announcement.objects.get(uuid=uuid)
                announcementUser = AnnouncementUser.objects.get(user=request.user, announcement=userAnnouncement)
                announcementUser.isRead = True
                announcementUser.read_date = datetime.date.today()
                announcementUser.save()

            responseData = dict()
            responseData['announcement'] = data.data

            return JsonResponse(responseData, safe=True)
        else:
            return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except Exception as e:

        return JsonResponse({'status': 'Fail', 'msg': e})
