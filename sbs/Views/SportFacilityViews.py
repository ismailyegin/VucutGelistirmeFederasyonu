import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import resolve
from unicode_tr import unicode_tr

from sbs.Forms.SportFacilityForm import SportFacilityForm
from sbs.Forms.havaspor.CommunicationForm import CommunicationForm
from sbs.Forms.havaspor.FacilityCommunicationForm import FacilityCommunicationForm
from sbs.Forms.havaspor.FacilitySearchForm import FacilitySearchForm
from sbs.Forms.havaspor.PersonForm import PersonForm
from sbs.Forms.havaspor.RefereeSearchForm import RefereeSearchForm
from sbs.Forms.havaspor.RefereeUserForm import RefereeUserForm
from sbs.Forms.havaspor.SportFacilityManagerForm import SportFacilityManagerForm
from sbs.Forms.havaspor.SportFacilityManagerPersonForm import SportFacilityManagerPersonForm
from sbs.models import Communication, Person, Coach, ReferenceSportFacility
from sbs.models.ekabis.City import City
from sbs.models.tvfbf.Branch import Branch
from sbs.models.tvfbf.DocumentName import DocumentName
from sbs.models.tvfbf.FacilityDocument import FacilityDocument
from sbs.models.tvfbf.SportFacilityManager import SportFacilityManager
from sbs.models.ekabis.Permission import Permission
from sbs.models.tvfbf.SportFacility import SportFacility
from sbs.services import general_methods
from sbs.services.services import last_urls


@login_required
def AddSportFacility(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    facilityForm = SportFacilityForm()
    manager_communication_form = FacilityCommunicationForm()

    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    if request.method == 'POST':

        facilityForm = SportFacilityForm(request.POST or None, request.FILES or None)
        manager_communication_form = FacilityCommunicationForm(request.POST or None, request.FILES)

        try:
            with transaction.atomic():
                if facilityForm.is_valid() and manager_communication_form.is_valid() :


                    managerCommunication = manager_communication_form.save(commit=False)
                    managerCommunication.save()

                    sportFacility = facilityForm.save(commit=False)
                    sportFacility.communication = managerCommunication
                    sportFacility.save()
                    documentNames=DocumentName.objects.all()
                    for name in documentNames:
                        facilityDocument=FacilityDocument(name=name)
                        facilityDocument.save()
                        sportFacility.document.add(facilityDocument)

                    log = str(facilityForm.cleaned_data['name']) + " Özel Spor Tesisi eklendi"
                    log = general_methods.logwrite(request, request.user, log)

                    messages.success(request, 'Özel Spor Tesisi Başarıyla Kayıt Edilmiştir.')

                    return redirect('sbs:AddSportFacility')

                else:

                    messages.warning(request, 'Alanları Kontrol Ediniz')
            return render(request, 'TVGFBF/SportFacility/add_sportFacility.html',
                          {'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'manager_communication_form': manager_communication_form,

                           'facilityForm': facilityForm,})


        except Exception as e:
            messages.warning(request, 'HATA !! ' + ' ' + str(e))
            return redirect('sbs:AddSportFacility')
    return render(request, 'TVGFBF/SportFacility/add_sportFacility.html',
                  {'urls': urls, 'current_url': current_url,
                   'url_name': url_name, 'manager_communication_form': manager_communication_form,

                   'facilityForm': facilityForm, })


@login_required
def return_facility(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    facilities = SportFacility.objects.all()
    user_form = FacilitySearchForm()
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    city = City.objects.all()
    with transaction.atomic():
        if request.method == 'POST':
            user_form = FacilitySearchForm(request.POST)
            derbis = request.POST.get('derbis')
            name = request.POST.get('name')
            city = request.POST.get('city')

            if not (derbis or name or city):
                facilities = SportFacility.objects.all().filter(isDeleted=0)
            else:
                query = Q()
                if name:
                    query &= Q(name__icontains=name.title())
                if derbis:
                    query &= Q(derbis__icontains=derbis)
                if city:
                    query &= Q(communication__city__name__icontains=city)

                facilities = SportFacility.objects.filter(query).filter(isDeleted=0)
        else:
            print('else2')

        #facility_dict={}
        #facility_list=[]
        # for facility in facilities:
        #     is_ok=facility.document.filter(file__isnull=True)
        #     if not is_ok:
        #         facility_dict['document_is_ok']=True
        #     facility_dict['facility']=facility
        #     facility_list.append(facility_dict)


    return render(request, 'TVGFBF/SportFacility/facilities.html',
                  {'facilities': facilities, 'user_form': user_form, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name, 'cities': city})


@login_required
def delete_facility(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']

                obj = SportFacility.objects.get(uuid=uuid)
                obj.delete()

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def update_sport_facility(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    facility = SportFacility.objects.get(uuid=uuid)
    facilityForm = SportFacilityForm(request.POST or None, request.FILES or None, instance=facility)
    communication = Communication.objects.get(pk=facility.communication.pk)
    manager_communication_form = FacilityCommunicationForm(request.POST or None, request.FILES or None,instance=communication)
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    if request.method == 'POST':

        try:
            with transaction.atomic():
                if facilityForm.is_valid() and manager_communication_form.is_valid():

                    facilityForm.save()
                    manager_communication_form.save()

                    log = str(facilityForm.cleaned_data['name']) + " Özel Spor Tesisi düzenlendi"
                    log = general_methods.logwrite(request, request.user, log)

                    messages.success(request, 'Özel Spor Tesisi Başarıyla Kayıt Edilmiştir.')

                    return redirect('sbs:return_facility')

                else:

                    messages.warning(request, 'Alanları Kontrol Ediniz')
            return render(request, 'TVGFBF/SportFacility/add_sportFacility.html',
                          {'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'manager_communication_form': manager_communication_form,

                           'facilityForm': facilityForm, })


        except Exception as e:
            messages.warning(request, 'HATA !! ' + ' ' + str(e))
            return redirect('sbs:return_facility')
    return render(request, 'TVGFBF/SportFacility/add_sportFacility.html',
                  {'urls': urls, 'current_url': current_url,
                   'url_name': url_name, 'manager_communication_form': manager_communication_form,

                   'facilityForm': facilityForm, })


@login_required
def return_facilityUser(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    facility = SportFacility.objects.get(uuid=uuid)
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    return render(request, 'TVGFBF/SportFacility/facility_manager_list.html',
                  {'facility': facility, 'urls': urls, 'current_url': current_url, 'url_name': url_name, })


@login_required
def return_facilityCoach(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    facility = SportFacility.objects.get(uuid=uuid)
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    return render(request, 'TVGFBF/SportFacility/facility_coach_list.html',
                  {'facility': facility, 'urls': urls, 'current_url': current_url, 'url_name': url_name, })


@login_required
def delete_facility_manager(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']

                obj = SportFacilityManager.objects.get(uuid=uuid)
                facility = SportFacility.objects.get(manager=obj)
                facility.manager.remove(obj)

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def delete_facility_coach(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                obj = Coach.objects.get(uuid=uuid)
                facility = SportFacility.objects.get(coach=obj)
                facility.coach.remove(obj)

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def AddSportFacilityManager(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    facility = SportFacility.objects.get(uuid=uuid)
    facilitymanagerForm = SportFacilityManagerForm()
    manager_communication_form = FacilityCommunicationForm()
    manager_person_form = SportFacilityManagerPersonForm()
    urls = last_urls(request)
    user_form = RefereeUserForm()
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    if request.method == 'POST':

        manager_communication_form = FacilityCommunicationForm(request.POST or None, request.FILES)
        manager_person_form = SportFacilityManagerPersonForm(request.POST or None, request.FILES or None)
        user_form = RefereeUserForm(request.POST or None, request.FILES)
        facilitymanagerForm = SportFacilityManagerForm(request.POST or None, request.FILES or None)

        try:
            with transaction.atomic():
                if user_form.is_valid() and manager_person_form.is_valid() and manager_communication_form.is_valid() and facilitymanagerForm.is_valid():

                    manager = SportFacilityManager()

                    managerUser = User()
                    managerUser.username = user_form.cleaned_data['email']
                    managerUser.first_name = unicode_tr(user_form.cleaned_data['first_name']).upper()
                    managerUser.last_name = unicode_tr(user_form.cleaned_data['last_name']).upper()
                    managerUser.email = user_form.cleaned_data['email']
                    # group = Group.objects.get(name='Spor Tesisi')
                    # password = User.objects.make_random_password()
                    # managerUser.set_password(password)
                    # managerUser.is_active = True
                    # managerUser.save()
                    # managerUser.groups.add(group)
                    managerUser.save()

                    person = manager_person_form.save(commit=False)
                    managerCommunication = manager_communication_form.save(commit=False)
                    managerCommunication.save()

                    person.user = managerUser
                    person.save()

                    manager.person = person

                    manager.personalityType = facilitymanagerForm.cleaned_data['personalityType']
                    manager.save()
                    branches = request.POST.getlist('branch')
                    for branch in branches:
                        manager.branch.add(Branch.objects.get(pk=int(branch)))

                    facility.manager.add(manager)
                    messages.success(request, 'Yetkili Başarıyla Kayıt Edilmiştir.')

                    return redirect('sbs:return_facilityUser', facility.uuid)

                else:

                    messages.warning(request, 'Alanları Kontrol Ediniz')
            return render(request, 'TVGFBF/SportFacility/add_facility_manager.html',
                          {'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'manager_communication_form': manager_communication_form,
                           'manager_person_form': manager_person_form,
                           'facilitymanagerForm': facilitymanagerForm, 'user_form': user_form, 'facility': facility})


        except Exception as e:
            messages.warning(request, 'HATA !! ' + ' ' + str(e))
            return redirect('sbs:return_facilityUser', facility.uuid)
    return render(request, 'TVGFBF/SportFacility/add_facility_manager.html',
                  {'urls': urls, 'current_url': current_url,
                   'url_name': url_name, 'manager_communication_form': manager_communication_form,
                   'manager_person_form': manager_person_form,
                   'facilitymanagerForm': facilitymanagerForm, 'user_form': user_form, 'facility': facility})

@login_required
def updateSportFacilityManager(request, uuid,facility_uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    facility=SportFacility.objects.get(uuid=facility_uuid)
    manager = SportFacilityManager.objects.get(uuid=uuid)
    manager_communication_form = FacilityCommunicationForm(request.POST or None, request.FILES or None,instance=manager.communication)
    manager_person_form = SportFacilityManagerPersonForm(request.POST or None, request.FILES or None,instance=manager.person)
    user=manager.person.user
    user_form = RefereeUserForm(request.POST or None,instance=user)
    facilitymanagerForm = SportFacilityManagerForm(request.POST or None, request.FILES or None,instance=manager)
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    if request.method == 'POST':
        try:
            with transaction.atomic():
                if user_form.is_valid() and manager_person_form.is_valid() and manager_communication_form.is_valid() and facilitymanagerForm.is_valid():


                    managerUser =manager.person.user
                    managerUser.username = user_form.cleaned_data['email']
                    managerUser.first_name = unicode_tr(user_form.cleaned_data['first_name']).upper()
                    managerUser.last_name = unicode_tr(user_form.cleaned_data['last_name']).upper()
                    managerUser.email = user_form.cleaned_data['email']
                    # group = Group.objects.get(name='Spor Tesisi')
                    # password = User.objects.make_random_password()
                    # managerUser.set_password(password)
                    # managerUser.is_active = True
                    # managerUser.save()
                    # managerUser.groups.add(group)
                    managerUser.save()

                    person = manager_person_form.save(commit=False)
                    managerCommunication = manager_communication_form.save(commit=False)
                    managerCommunication.save()

                    person.user = managerUser
                    person.save()

                    manager.person = person

                    manager.personalityType = facilitymanagerForm.cleaned_data['personalityType']
                    manager.save()
                    branches = request.POST.getlist('branch')
                    for branch in branches:
                        manager.branch.add(Branch.objects.get(pk=int(branch)))

                    messages.success(request, 'Yetkili Başarıyla Kayıt Edilmiştir.')

                    return redirect('sbs:return_facilityUser', facility_uuid)

                else:

                    messages.warning(request, 'Alanları Kontrol Ediniz')
            return render(request, 'TVGFBF/SportFacility/add_facility_manager.html',
                          {'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'manager_communication_form': manager_communication_form,
                           'manager_person_form': manager_person_form,
                           'facilitymanagerForm': facilitymanagerForm, 'user_form': user_form, 'facility': facility})


        except Exception as e:
            messages.warning(request, 'HATA !! ' + ' ' + str(e))
            return redirect('sbs:return_facilityUser', facility_uuid)
    return render(request, 'TVGFBF/SportFacility/add_facility_manager.html',
                  {'urls': urls, 'current_url': current_url,
                   'url_name': url_name, 'manager_communication_form': manager_communication_form,
                   'manager_person_form': manager_person_form,
                   'facilitymanagerForm': facilitymanagerForm, 'user_form': user_form, 'facility': facility})


@login_required
def AddSportFacilityCoach(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    facility = SportFacility.objects.get(uuid=uuid)
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    coaches = Coach.objects.all()
    if request.method == 'POST':
        try:
            with transaction.atomic():
                if request.POST['coach'] != '':
                    coaches = request.POST.getlist('coach')
                    for coach in coaches:
                        facility.coach.add(Coach.objects.get(uuid=coach))

                messages.success(request, 'Çalıştırıcı Başarıyla Kayıt Edilmiştir.')

                return redirect('sbs:return_facilityCoach', facility.uuid)



        except Exception as e:
            messages.warning(request, 'HATA !! ' + ' ' + str(e))
            return redirect('sbs:return_facilityCoach', facility.uuid)
    return render(request, 'TVGFBF/SportFacility/add_facility_coach.html',
                  {'urls': urls, 'current_url': current_url,
                   'url_name': url_name, 'facility': facility, 'coachs': coaches})



@login_required
def return_facilityDocument(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    facility = SportFacility.objects.get(uuid=uuid)
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    if request.method == 'POST':
        try:
            with transaction.atomic():

                for file in request.FILES:
                    if facility.document.filter(name__name=file):
                        document=facility.document.get(name__name=file)
                        doc = request.FILES[''+str(document.name.name)+'']
                        document.file=doc
                        document.save()

                messages.success(request, 'Belgeler Başarıyla Kayıt Edilmiştir.')

                return redirect('sbs:return_facilityDocument', facility.uuid)



        except Exception as e:
            messages.warning(request, 'HATA !! ' + ' ' + str(e))
            return redirect('sbs:return_facilityDocument', facility.uuid)

    return render(request, 'TVGFBF/SportFacility/facility_document_list.html',
                  {'facility': facility, 'urls': urls, 'current_url': current_url, 'url_name': url_name, })


@login_required
def delete_facility_document(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                obj = FacilityDocument.objects.get(uuid=uuid)
                obj.file=None
                obj.save()

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def pre_facility(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    facilities = ReferenceSportFacility.objects.filter(isDeleted=False)
    user_form = FacilitySearchForm()
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    city = City.objects.all()
    return render(request, 'TVGFBF/SportFacility/facility_application_list.html',
                  {'facilities': facilities, 'user_form': user_form, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name, 'cities': city})


@login_required
def pre_facility_approve(request,uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    with transaction.atomic():
        if request.method == 'POST':
            pre_facility = ReferenceSportFacility.objects.get(uuid=uuid)
            spor_facility = SportFacility.objects.get(derbis=pre_facility.derbis)
            spor_facility.name = pre_facility
            spor_facility.registrationNumber = pre_facility.registrationNumber
            spor_facility.taxNumber = pre_facility.taxNumber
            spor_facility.communication = pre_facility.coordinate
            spor_facility.mersis = pre_facility.mersis

            spor_facility.save()
            pre_facility.isDeleted = True
            pre_facility.save()

            messages.success(request, 'Özel Spor Salonu Kayıt Edilmiştir.')

            return redirect('sbs:return_facility')

        else:
            print('else2')
            return redirect('sbs:return_facility')


