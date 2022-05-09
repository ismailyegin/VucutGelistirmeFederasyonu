import traceback
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import resolve
from sbs.Forms.PermissionForm import PermissionForm
from sbs.models.ekabis.Permission import Permission
from sbs.services import general_methods
from sbs.services.general_methods import get_error_messages
from sbs.services.services import last_urls

import inspect
from sbs.Views.ekabis import AdminViews, GroupView


@login_required
def view_permission(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        return render(request, 'Permission/view_permission.html',
                      {'urls': urls, 'current_url': current_url, 'url_name': url_name.name})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def change_permission(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:

        permission = Permission.objects.get(uuid=uuid)
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        permission_form = PermissionForm(request.POST or None, instance=permission)
        # Bu alan sistem çalışmasından sonra silinecegi icin kod düzenlemsinde cast edilmesinde önem verilmedi
        urls = []
        from sbs.urls import urlpatterns
        view_url = ""
        for urlpattern in urlpatterns:
            if urlpattern.name == permission.codename:
                view_url = urlpattern.lookup_str
        url = view_url.split('.')

        code = change_permission
        if url[0] == 'sbs':
            if url[2] == 'AdminViews':
                result = getattr(AdminViews, url[3])
                code = inspect.getsource(result)
            elif url[2] == 'GroupView':
                result = getattr(GroupView, url[3])
                code = inspect.getsource(result)

        with transaction.atomic():
            if request.method == 'POST':
                if permission_form.is_valid():
                    perm = permission_form.save(request, commit=False)
                    perm.save()
                    messages.success(request, 'İzin Güncellenmiştir.')
                    return redirect('sbs:view_permission')
                else:
                    error_messages = get_error_messages(permission_form)
                    return render(request, 'Permission/change_permission.html',
                                  {
                                      'urls': urls,
                                      'current_url': current_url,
                                      'url_name': url_name,
                                      'error_messages': error_messages,
                                      'permission_form': permission_form,
                                      'code': code
                                  })
            return render(request, 'Permission/change_permission.html',
                          {'urls': urls,
                           'current_url': current_url, 'url_name': url_name,
                           'permission_form': permission_form,
                           'code': code
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')
