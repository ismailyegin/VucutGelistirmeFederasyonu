import traceback

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import resolve

from sbs.Forms.GroupForm import GroupForm
from sbs.models.ekabis.Permission import Permission
from sbs.models.ekabis.PermissionGroup import PermissionGroup
from sbs.services import general_methods
from sbs.services.general_methods import get_error_messages
from sbs.services.services import GroupService, PermissionService, PermissionGroupService, GroupGetService, last_urls

# add a group to the system
@login_required
def add_group(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    group_form = GroupForm()
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    try:
        with transaction.atomic():
            if request.method == 'POST':
                group_form = GroupForm(request.POST)
                if group_form.is_valid():
                    group = group_form.save(request, commit=False)
                    group.save()

                    for item in PermissionService(request, None):
                        permissionGroupfilter = {
                            'group': group,
                            'permissions': item
                        }
                        if not (PermissionGroupService(request, permissionGroupfilter)):
                            perm = PermissionGroup(group=group, permissions=item, is_active=False)
                            perm.save()

                    messages.success(request, 'Grup Kayıt Edilmiştir.')
                    return redirect('sbs:view_group')
                else:
                    error_messages = get_error_messages(group_form)
                    return render(request, 'Group/GrupEkle.html',
                                  {'group_form': group_form, 'error_messages': error_messages, 'urls': urls,
                                   'current_url': current_url, 'url_name': url_name})
            return render(request, 'Group/GrupEkle.html',
                          {'group_form': group_form, 'error_messages': '', 'urls': urls, 'current_url': current_url,
                           'url_name': url_name})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def return_list_group(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:

        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        groups = GroupService(request, None)
        return render(request, 'Group/GrupListe.html',
                      {'groups': groups, 'urls': urls, 'current_url': current_url, 'url_name': url_name})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('sbs:view_group')

# group update to system
@login_required
def return_update_group(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        groupfilter = {
            'pk': pk
        }
        groups = GroupGetService(request, groupfilter)
        group_form = GroupForm(request.POST or None, instance=groups)
        with transaction.atomic():
            if request.method == 'POST':
                if group_form.is_valid():
                    group=group_form.save(request, commit=False)
                    group.save()
                    messages.success(request, 'Grup Güncellenmiştir.')
                    return redirect('sbs:view_group')

                else:
                    error_messages = get_error_messages(group_form)
                    return render(request, 'Group/grupGuncelle.html',
                                  {'group_form': group_form, 'error_messages': error_messages, 'urls': urls,
                                   'current_url': current_url, 'url_name': url_name
                                   })

            return render(request, 'Group/grupGuncelle.html',
                          {'group_form': group_form, 'error_messages': '', 'urls': urls, 'current_url': current_url,
                           'url_name': url_name
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')

# group permission update
def change_groupPermission(request, pk):
    perm = general_methods.control_access(request)
    active = general_methods.controlGroup(request)
    if not perm:
        print('ex')
        # logout(request)
        # return redirect('accounts:login')
    groupfilter = {
        'group__id': pk
    }
    permGroup = PermissionGroupService(request, groupfilter)
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':
                for item in permGroup:
                    if request.POST.get(str(item.pk)):
                        item.is_active = True
                    else:
                        item.is_active = False
                    item.save()
            return render(request, 'Group/GrupizinEkle.html',
                          {'permGroup': permGroup, 'urls': urls, 'current_url': current_url, 'url_name': url_name,
                           'active': active})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
