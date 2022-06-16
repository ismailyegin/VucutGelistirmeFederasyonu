import datetime
import traceback
from datetime import date
from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core import serializers
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.urls import resolve
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from unicode_tr import unicode_tr
from zeep import Client

from accounts.models import Forgot
from sbs.Forms.CategoryItemForm import CategoryItemForm
from sbs.Forms.UserForm import UserForm
from sbs.Forms.havaspor.CommunicationForm import CommunicationForm
from sbs.Forms.havaspor.GradeFormReferee import GradeFormReferee
from sbs.Forms.havaspor.PersonForm import PersonForm
from sbs.Forms.havaspor.PreRefereeForm import PreRefereeForm
from sbs.Forms.havaspor.RefereeForm import RefereeForm
from sbs.Forms.havaspor.RefereeSearchForm import RefereeSearchForm
from sbs.Forms.havaspor.HavaUserForm import HavaUserForm
from sbs.Forms.havaspor.VisaForm import VisaForm
from sbs.Forms.havaspor.VisaSeminarForm import VisaSeminarForm
from sbs.models.ekabis.EnumFields import EnumFields
from sbs.models.ekabis.CategoryItem import CategoryItem
from sbs.models.ekabis.Communication import Communication
from sbs.models.ekabis.Logs import Logs
from sbs.models.ekabis.Person import Person
from sbs.models.ekabis.Permission import Permission
from sbs.models.tvfbf.Branch import Branch
from sbs.models.tvfbf.PreRegistration import PreRegistration
from sbs.models.tvfbf.RefereeApplication import RefereeApplication
from sbs.models.tvfbf.ReferenceReferee import ReferenceReferee
from sbs.models.tvfbf.VisaSeminar import VisaSeminar
from sbs.models.tvfbf.HavaLevel import HavaLevel
from sbs.models.tvfbf.Referee import Referee
from sbs.services import general_methods
from sbs.services.general_methods import get_client_ip
from sbs.services.services import last_urls


@login_required
def return_referees(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user_form = RefereeSearchForm()
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    current_date = datetime.date.today()
    return render(request, 'TVGFBF/Referee/referees.html',
                  {'user_form': user_form, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name, 'current_date': current_date, })


@login_required
def return_referee_search(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    referees = Referee.objects.filter(infoStatus=1, isDeleted=0)
    user_form = RefereeSearchForm()
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    current_date = datetime.date.today()
    with transaction.atomic():
        if request.method == 'POST':
            user_form = RefereeSearchForm(request.POST)
            branch = request.POST.get('branch')
            status = request.POST.get('status')
            city = request.POST.get('city')
            firstName = unicode_tr(request.POST.get('first_name'))
            lastName = unicode_tr(request.POST.get('last_name'))

            # print(firstName, lastName, email, branch, grade, visa)
            if not (firstName or lastName or city or branch or status):
                return redirect('sbs:return_referees')
            else:
                query = Q()
                if lastName:
                    query &= Q(person__user__last_name__icontains=lastName.upper())
                if firstName:
                    query &= Q(person__user__first_name__icontains=firstName.upper())
                if city:
                    query &= Q(communication__city__name__icontains=city)
                if branch:
                    query &= Q(grades__branch=Branch.objects.get(title=branch))
                if status:
                    query &= Q(grades__definition__name=status)

                referees = Referee.objects.filter(query).filter(isDeleted=0)
        else:
            print('else2')

    return render(request, 'TVGFBF/Referee/refereeSearch.html',
                  {'referees': referees, 'user_form': user_form, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name, 'current_date': current_date, })


@login_required
def return_add_referee(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user_form = HavaUserForm()
    person_form = PersonForm()
    #
    # country = Country.objects.filter(name="TÜRKİYE")[0]
    # communication_form = CommunicationForm(initial={'country': country})
    communication_form = CommunicationForm()
    referee_form = RefereeForm()
    grade_form = GradeFormReferee()

    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    with transaction.atomic():
        if request.method == 'POST':

            user_form = HavaUserForm(request.POST)
            person_form = PersonForm(request.POST, request.FILES or None)
            communication_form = CommunicationForm(request.POST)
            referee_form = RefereeForm(request.POST, request.FILES or None)
            grade_form = GradeFormReferee(request.POST, request.FILES or None)

            mail = request.POST.get('email')

            # if User.objects.filter(email=mail):
            #     messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
            #     return render(request, 'TVGFBF/Referee/add-referee.html',
            #                   {'user_form': user_form, 'person_form': person_form,
            #                    'communication_form': communication_form, 'grade_form': grade_form, })

            tc = request.POST.get('tc')
            # if Person.objects.filter(tc=tc):
            #     messages.warning(request, 'Tc kimlik numarasi sisteme kayıtlıdır. ')
            #     return render(request, 'TVGFBF/Referee/add-referee.html',
            #                   {'user_form': user_form, 'person_form': person_form,
            #                    'communication_form': communication_form, 'grade_form': grade_form, })

            name = request.POST.get('first_name')
            surname = request.POST.get('last_name')
            year = request.POST.get('birthDate')
            year = year.split('/')

            # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
            # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
            #     messages.warning(request, 'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
            #     return render(request, 'TVGFBF/Referee/add-referee.html',
            #                   {'user_form': user_form, 'person_form': person_form,
            #                    'communication_form': communication_form, 'grade_form': grade_form, })

            if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid() and grade_form.is_valid() and referee_form.is_valid():
                user = User()
                user.username = user_form.cleaned_data['email']

                user.first_name = unicode_tr(user_form.cleaned_data['first_name']).upper()
                user.last_name = unicode_tr(user_form.cleaned_data['last_name']).upper()
                user.email = user_form.cleaned_data['email']
                group = Group.objects.get(name='Hakem')
                password = User.objects.make_random_password()
                user.set_password(password)
                user.is_active = True
                user.save()

                user.groups.add(group)
                user.save()

                person = person_form.save(commit=False)
                communication = communication_form.save(commit=False)
                iban = request.POST.get("iban")
                person.iban = iban
                person.user = user
                person.save()
                communication.save()
                grade = grade_form.save()
                grade.save()

                referee = referee_form.save(commit=False)
                referee.person = person
                referee.communication = communication
                referee.save()
                referee.grades.add(grade)  ####!!!!!
                referee.save()

                fdk = Forgot(user=user, status=False)
                fdk.save()

                # html_content = ''
                # subject, from_email, to = 'Bilgi Sistemi Kullanıcı Bilgileri', 'no-reply@badminton.gov.tr', user.email
                # html_content = '<h2>TÜRKİYE BADMİNTON FEDERASYONU BİLGİ SİSTEMİ</h2>'
                # html_content = html_content + '<p><strong>Kullanıcı Adınız :' + str(fdk.user.username) + '</strong></p>'
                # html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://sbs.badminton.gov.tr/newpassword?query=' + str(
                #     fdk.uuid) + '">http://sbs.badminton.gov.tr/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'
                # msg = EmailMultiAlternatives(subject, '', from_email, [to])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()

                messages.success(request, 'Hakem Başarıyla Kayıt Edilmiştir.')

                # return redirect('sbs:hakem-duzenle', referee.pk)
                return redirect('sbs:return_referees')

            else:

                for x in user_form.errors.as_data():
                    messages.warning(request, user_form.errors[x][0])

    return render(request, 'TVGFBF/Referee/add-referee.html',
                  {'user_form': user_form, 'person_form': person_form,
                   'communication_form': communication_form, 'referee_form': referee_form, 'grade_form': grade_form,
                   'urls': urls, 'current_url': current_url, 'url_name': url_name, })


@login_required
def update_referee(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    referee = Referee.objects.get(uuid=uuid)
    user = User.objects.get(pk=referee.person.user.pk)
    person = Person.objects.get(pk=referee.person.pk)
    communication = Communication.objects.get(pk=referee.communication.pk)
    user_form = HavaUserForm(request.POST or None, instance=user)
    person_form = PersonForm(request.POST or None, request.FILES or None, instance=person)
    person_form.fields['profileImage'].required = True
    communication_form = CommunicationForm(request.POST or None, instance=communication)

    grade_form = referee.grades.filter(isDeleted=0)
    visa_form = referee.visa.filter(isDeleted=0)

    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    with transaction.atomic():
        if request.method == 'POST':

            mail = request.POST.get('email')
            # if mail != referee.user.email:
            #
            #     if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
            #             email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
            #         email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
            #         email=mail):
            #         messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
            #         return render(request, 'TVGFBF/Referee/update-referee.html',
            #                       {'user_form': user_form, 'communication_form': communication_form,
            #                        'person_form': person_form, 'judge': judge, 'grade_form': grade_form,
            #                        'visa_form': visa_form, 'iban_form': iban_form, })

            tc = request.POST.get('tc')
            # if tc != referee.person.tc:
            #     if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
            #             tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
            #         tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
            #         messages.warning(request, 'Tc kimlik numarasi sisteme kayıtlıdır. ')
            #         return render(request, 'TVGFBF/Referee/update-referee.html',
            #                       {'user_form': user_form, 'communication_form': communication_form,
            #                        'person_form': person_form, 'judge': judge, 'grade_form': grade_form,
            #                        'visa_form': visa_form, 'iban_form': iban_form, })

            name = request.POST.get('first_name')
            surname = request.POST.get('last_name')
            year = request.POST.get('birthDate')
            year = year.split('/')

            # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
            # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
            #     messages.warning(request, 'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
            #     return render(request, 'TVGFBF/Referee/update-referee.html',
            #                   {'user_form': user_form, 'communication_form': communication_form,
            #                    'person_form': person_form, 'referee': referee, 'grade_form': grade_form,
            #                    'visa_form': visa_form, })

            if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid():

                user.username = user_form.cleaned_data['email']
                user.first_name = user_form.cleaned_data['first_name']
                user.last_name = user_form.cleaned_data['last_name']
                user.email = user_form.cleaned_data['email']
                user.save()

                log = str(user.get_full_name()) + " Hakemi güncelledi"
                log = general_methods.logwrite(request, request.user, log)

                person = person_form.save(commit=False)
                iban = request.POST.get("iban")
                person.iban = iban
                person.save()
                communication_form.save()

                messages.success(request, 'Hakem Başarıyla Güncellendi')
                return redirect('sbs:return_referees')
            else:
                messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'TVGFBF/Referee/update-referee.html',
                  {'user_form': user_form, 'communication_form': communication_form,
                   'person_form': person_form, 'referee': referee, 'grade_form': grade_form,
                   'visa_form': visa_form, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name, })


@login_required
def delete_referee(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']

                obj = Referee.objects.get(uuid=uuid)
                data_as_json_pre = serializers.serialize('json', Referee.objects.filter(uuid=uuid))

                obj.isDeleted = True
                obj.save()
                log = "Hakem Sil"
                logs = Logs(user=request.user, subject=log, ip=get_client_ip(request),
                            previousData=data_as_json_pre)
                logs.save()

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def add_grade_referee(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    referee = Referee.objects.get(uuid=uuid)
    grade_form = GradeFormReferee()
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    with transaction.atomic():
        if request.method == 'POST':
            grade_form = GradeFormReferee(request.POST, request.FILES)

            if grade_form.is_valid() and grade_form.cleaned_data['dekont'] is not None and request.POST.get(
                    'branch') is not None:
                grade = HavaLevel(definition=grade_form.cleaned_data['definition'],
                                  startDate=grade_form.cleaned_data['startDate'],
                                  dekont=grade_form.cleaned_data['dekont'],
                                  branch=grade_form.cleaned_data['branch'])
                grade.levelType = EnumFields.LEVELTYPE.GRADE
                grade.status = HavaLevel.WAITED
                grade.isActive = True
                grade.save()
                for item in referee.grades.all():
                    if item.branch == grade.branch:
                        item.isActive = False
                        item.save()

                referee.grades.add(grade)
                referee.save()

                log = str(referee.person.user.get_full_name()) + " Kademe eklendi"
                log = general_methods.logwrite(request, request.user, log)

                messages.success(request, 'Kademe Başarıyla Eklenmiştir.')
                return redirect('sbs:update_referee', uuid=uuid)

            else:
                messages.warning(request, 'Alanları Kontrol Ediniz')

    grade_form.fields['definition'].queryset = CategoryItem.objects.filter(forWhichClazz='REFEREE_GRADE')
    return render(request, 'TVGFBF/Referee/add-grade-referee.html',
                  {'grade_form': grade_form, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name, })


@login_required
def grade_approval(request, grade_uuid, referee_uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade = HavaLevel.objects.get(uuid=grade_uuid)
    referee = Referee.objects.get(uuid=referee_uuid)
    try:
        for item in referee.grades.all():
            if item.branch == grade.branch:
                item.isActive = False
                item.save()
        grade.status = HavaLevel.APPROVED
        grade.isActive = True
        grade.save()

        log = str(referee.person.user.get_full_name()) + " Kademe onaylandi"
        log = general_methods.logwrite(request, request.user, log)

        messages.success(request, 'Kademe   Onaylanmıştır')
    except:
        messages.warning(request, 'Lütfen yeniden deneyiniz.')
    return redirect('sbs:update_referee', uuid=referee_uuid)


@login_required
def grade_reject(request, grade_uuid, referee_uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade = HavaLevel.objects.get(uuid=grade_uuid)
    grade.status = HavaLevel.DENIED
    grade.save()

    referee = Referee.objects.get(uuid=referee_uuid)
    log = str(referee.person.user.get_full_name()) + " Kademe reddedildi"
    log = general_methods.logwrite(request, request.user, log)

    messages.success(request, 'Kademe Reddedilmiştir')
    return redirect('sbs:update_referee', uuid=referee_uuid)


@login_required
def update_grade(request, grade_uuid, referee_uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade = HavaLevel.objects.get(uuid=grade_uuid)
    referee = Referee.objects.get(uuid=referee_uuid)
    grade_form = GradeFormReferee(request.POST or None, request.FILES or None, instance=grade,
                                  initial={'definition': grade.definition})
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    if request.method == 'POST':
        if grade_form.is_valid():
            grade_form.save()
            if grade.status != HavaLevel.APPROVED:
                grade.status = HavaLevel.WAITED
                grade.save()

                log = str(referee.person.user.get_full_name()) + " Kademe guncellendi"
                log = general_methods.logwrite(request, request.user, log)
            messages.success(request, 'Kademe Başarılı bir şekilde güncellenmiştir.')
            return redirect('sbs:update_referee', uuid=referee_uuid)

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'TVGFBF/Referee/update-grade-referee.html',
                  {'grade_form': grade_form, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name, })


@login_required
def delete_grade(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                grade_uuid = request.POST['grade_uuid']
                referee_uuid = request.POST['referee_uuid']

                obj = HavaLevel.objects.get(uuid=grade_uuid)
                referee = Referee.objects.get(uuid=referee_uuid)

                data_as_json_pre = serializers.serialize('json', Referee.objects.filter(uuid=referee_uuid))

                obj.isDeleted = True
                obj.save()
                log = "Hakem Kademe Sil"
                logs = Logs(user=request.user, subject=log, ip=get_client_ip(request),
                            previousData=data_as_json_pre)
                logs.save()

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


def add_visa_referee(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    referee = Referee.objects.get(uuid=uuid)
    visa_form = VisaForm()
    category_item_form = CategoryItemForm()
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    with transaction.atomic():
        if request.method == 'POST':
            visa_form = VisaForm(request.POST, request.FILES)
            category_item_form = CategoryItemForm(request.POST, request.FILES)

            try:
                if visa_form.is_valid():

                    visa = HavaLevel(dekont=visa_form.cleaned_data['dekont'], branch=visa_form.cleaned_data['branch'])
                    visa.startDate = visa_form.cleaned_data['startDate']

                    visa.definition = CategoryItem.objects.get(forWhichClazz='VISA_REFEREE')
                    visa.levelType = EnumFields.LEVELTYPE.VISA
                    visa.status = HavaLevel.WAITED
                    for item in referee.visa.all():
                        if item.branch == visa.branch:
                            item.isActive = False
                            item.save()
                    visa.isActive = True

                    visa.save()
                    referee.visa.add(visa)
                    referee.save()

                    log = str(referee.person.user.get_full_name()) + " hakem  vize eklendi"
                    log = general_methods.logwrite(request, request.user, log)

                    messages.success(request, 'Vize Başarıyla Eklenmiştir.')
                    return redirect('sbs:update_referee', uuid=uuid)
            except:
                messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'TVGFBF/Referee/add-visa-referee.html',
                  {'visa_form': visa_form, 'category_item_form': category_item_form, 'urls': urls,
                   'current_url': current_url,
                   'url_name': url_name, })


@login_required
def visa_approval(request, visa_uuid, referee_uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    visa = HavaLevel.objects.get(uuid=visa_uuid)
    visa.status = HavaLevel.APPROVED
    visa.save()
    referee = Referee.objects.get(uuid=referee_uuid)
    log = str(referee.person.user.get_full_name()) + " vize onaylandi"
    log = general_methods.logwrite(request, request.user, log)

    messages.success(request, 'Vize onaylanmıştır.')
    return redirect('sbs:update_referee', uuid=referee_uuid)


@login_required
def visa_reject(request, visa_uuid, referee_uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    visa = HavaLevel.objects.get(uuid=visa_uuid)
    visa.status = HavaLevel.DENIED
    visa.save()
    referee = Referee.objects.get(uuid=referee_uuid)
    log = str(referee.person.user.get_full_name()) + " vize reddedildi"
    log = general_methods.logwrite(request, request.user, log)

    messages.warning(request, 'Vize Reddedilmiştir.')
    return redirect('sbs:update_referee', uuid=referee_uuid)


@login_required
def visa_update(request, visa_uuid, referee_uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    visa = HavaLevel.objects.get(uuid=visa_uuid)
    referee = Referee.objects.get(uuid=referee_uuid)
    visa_form = VisaForm(request.POST or None, request.FILES or None, instance=visa)
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    with transaction.atomic():
        if request.method == 'POST':
            if visa_form.is_valid():
                visa_form.save()
                if visa.status != HavaLevel.APPROVED:
                    visa.status = HavaLevel.WAITED
                    visa.save()

                    log = str(referee.person.user.get_full_name()) + " hakem  vize güncellendi"
                    log = general_methods.logwrite(request, request.user, log)

                    messages.success(request, 'Vize Başarıyla Güncellenmiştir.')
                    return redirect('sbs:update_referee', uuid=referee_uuid)
            else:
                messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'TVGFBF/Referee/update-visa-referee.html',
                  {'visa_form': visa_form,'urls':urls,'current_url':current_url,'url_name':url_name})


@login_required
def visa_delete(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                visa_uuid = request.POST['visa_uuid']
                referee_uuid = request.POST['referee_uuid']

                obj = HavaLevel.objects.get(uuid=visa_uuid)
                referee = Referee.objects.get(uuid=referee_uuid)

                data_as_json_pre = serializers.serialize('json', Referee.objects.filter(uuid=referee_uuid))

                obj.isDeleted = True
                obj.save()
                log = "Hakem Vize Sil"
                logs = Logs(user=request.user, subject=log, ip=get_client_ip(request),
                            previousData=data_as_json_pre)
                logs.save()

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def return_level(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    category_item_form = CategoryItemForm()
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    with transaction.atomic():
        if request.method == 'POST':

            category_item_form = CategoryItemForm(request.POST)

            if category_item_form.is_valid():

                categoryItem = CategoryItem(name=category_item_form.cleaned_data['name'])
                categoryItem.forWhichClazz = "REFEREE_GRADE"
                categoryItem.save()

                return redirect('sbs:return_levels')

            else:

                messages.warning(request, 'Alanları Kontrol Ediniz')
    categoryitem = CategoryItem.objects.filter(forWhichClazz="REFEREE_GRADE", isDeleted=0)
    return render(request, 'TVGFBF/Referee/levels.html',
                  {'category_item_form': category_item_form, 'categoryitem': categoryitem,
                   'urls':urls,'current_url':current_url,'url_name':url_name})


@login_required
def levelUpdate(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    categoryItem = CategoryItem.objects.get(uuid=uuid)
    category_item_form = CategoryItemForm(request.POST or None, instance=categoryItem)
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    with transaction.atomic():
        if request.method == 'POST':
            if category_item_form.is_valid():
                category = category_item_form.save(request, commit=False)
                category.save()
                messages.success(request, 'Başarıyla Güncellendi')
                return redirect('sbs:return_levels')
            else:
                messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'TVGFBF/Referee/update-level.html',
                  {'category_item_form': category_item_form,
                   'urls':urls,'current_url':current_url,'url_name':url_name})


def levelDelete(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                obj = CategoryItem.objects.get(uuid=uuid)
                obj.isDeleted = True
                obj.save()

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except CategoryItem.DoesNotExist:
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def gradeList(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    coa = []
    for item in CategoryItem.objects.filter(forWhichClazz='REFEREE_GRADE'):
        coa.append(item.pk)
    grade = HavaLevel.objects.filter(definition_id__in=coa, levelType=EnumFields.LEVELTYPE.GRADE,
                                     isDeleted=0).distinct()

    return render(request, 'TVGFBF/Referee/referee-grade-list.html',
                  {'refereeGrades': grade,'urls':urls,'current_url':current_url,'url_name':url_name})


@login_required
def gradeListApproval(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade = HavaLevel.objects.get(uuid=uuid)
    referee = grade.Refereegrades.first()
    try:
        for item in referee.grades.all():
            if item.branch == grade.branch:
                item.isActive = False
                item.save()
        grade.status = HavaLevel.APPROVED
        grade.isActive = True
        grade.save()
        messages.success(request, 'Kademe   Onaylanmıştır')
    except:
        messages.warning(request, 'Lütfen yeniden deneyiniz.')

    return redirect('sbs:grade_list')


@login_required
def gradeListReject(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade = HavaLevel.objects.get(uuid=uuid)
    grade.status = HavaLevel.DENIED
    grade.save()
    messages.success(request, 'Kademe  Reddedilmiştir.')
    return redirect('sbs:grade_list')


@login_required
def gradeListApprovalAll(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        coa = []
        for item in CategoryItem.objects.filter(forWhichClazz='REFEREE_GRADE'):
            coa.append(item.pk)
        grades = HavaLevel.objects.filter(definition_id__in=coa, levelType=EnumFields.LEVELTYPE.GRADE,
                                          status="Beklemede")

        for grade in grades:
            referee = grade.Refereegrades.first()
            if request.method == 'POST' and request.is_ajax():
                for item in referee.grades.all():
                    if item.branch == grade.branch:
                        item.isActive = False
                        item.save()
                grade.status = HavaLevel.APPROVED
                grade.isActive = True
                grade.save()
                return JsonResponse({'status': 'Success', 'msg': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def gradeListRejectAll(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        if request.method == 'POST' and request.is_ajax():
            coa = []
            for item in CategoryItem.objects.filter(forWhichClazz='REFEREE_GRADE'):
                coa.append(item.pk)
            grades = HavaLevel.objects.filter(definition_id__in=coa, levelType=EnumFields.LEVELTYPE.GRADE,
                                              status="Beklemede")
            for grade in grades:
                grade.status = HavaLevel.DENIED
                grade.save()
            return JsonResponse({'status': 'Success', 'msg': 'save successfully'})

        else:
            return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def visaList(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    coa = []
    for item in CategoryItem.objects.filter(forWhichClazz='VISA_REFEREE'):
        coa.append(item.pk)
    visa = HavaLevel.objects.filter(definition_id__in=coa, levelType=EnumFields.VISA).distinct()
    return render(request, 'TVGFBF/Referee/referee-visa-list.html',
                  {'refereevisas': visa,'urls':urls,'current_url':current_url,'url_name':url_name})


@login_required
def visaListApproval(request, uuid):
    try:
        perm = general_methods.control_access(request)

        if not perm:
            logout(request)
            return redirect('accounts:login')
        visa = HavaLevel.objects.get(uuid=uuid)
        visa.status = HavaLevel.APPROVED
        refere = visa.Refereevisa.first()
        for item in refere.visa.all():
            if item.branch == visa.branch:
                item.isActive = False
                item.save()
        visa.isActive = True
        visa.save()
        messages.success(request, 'Vize Onaylanmıştır.')
    except:
        messages.warning(request, 'Yeniden deneyiniz.')

    return redirect('sbs:visa_list')


@login_required
def visaListReject(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    visa = HavaLevel.objects.get(uuid=uuid)
    visa.status = HavaLevel.DENIED
    visa.save()
    messages.success(request, 'Vize reddedilmistir.')
    return redirect('sbs:visa_list')


@login_required
def returnVisaSeminar(request):
    perm = general_methods.control_access_referee(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    user = request.user
    seminar = VisaSeminar.objects.filter(forWhichClazz='REFEREE', isDeleted=0)
    with transaction.atomic():
        if request.method == 'POST':
            if user.groups.filter(name='Hakem').exists():
                vizeSeminer = VisaSeminar.objects.get(pk=request.POST.get('pk'))
                referee = Referee.objects.get(user=request.user)
                try:
                    if request.FILES['file']:
                        document = request.FILES['file']
                        data = RefereeApplication()
                        data.dekont = document
                        data.referee = referee
                        data.save()
                        vizeSeminer.refereeApplication.add(data)
                        vizeSeminer.save()

                        messages.success(request, 'Vize Seminerine Başvuru gerçekleşmiştir.')
                        return redirect('sbs:return-visa-seminar-application')
                except:
                    messages.warning(request, 'Lütfen yeniden deneyiniz')

    return render(request, 'TVGFBF/Referee/referee-visa-seminar.html', {'competitions': seminar,
                                                                        'urls':urls,'current_url':current_url,'url_name':url_name})


@login_required
def addVisaSeminar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    visaSeminar = VisaSeminarForm()
    with transaction.atomic():
        if request.method == 'POST':
            visaSeminar = VisaSeminarForm(request.POST)
            if visaSeminar.is_valid():

                visa = visaSeminar.save()
                visa.forWhichClazz = 'REFEREE'
                visa.save()
                messages.success(request, 'Vize Semineri Başari  Kaydedilmiştir.')

                return redirect('sbs:referee-visa-seminar')
            else:

                messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'TVGFBF/Referee/add-visa-seminar-referee.html',
                  {'competition_form': visaSeminar,'urls':urls,'current_url':current_url,'url_name':url_name})


@login_required
def updateVisaSeminar(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    seminar = VisaSeminar.objects.get(uuid=uuid)
    referee = seminar.referee.all()
    competition_form = VisaSeminarForm(request.POST or None, instance=seminar)
    with transaction.atomic():
        if request.method == 'POST':
            if competition_form.is_valid():
                competition_form.save()
                messages.success(request, 'Vize Seminer Başarıyla Güncellenmiştir.')

                return redirect('sbs:referee-visa-seminar')
            else:

                messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'TVGFBF/Referee/update-referee-visa-seminar.html',
                  {'competition_form': competition_form, 'competition': seminar, 'referees': referee})


@login_required
def visaSeminarApproval(request, uuid):
    seminar = VisaSeminar.objects.get(uuid=uuid)

    if seminar.status == VisaSeminar.WAITED:

        for item in seminar.referee.all():
            visa = HavaLevel(dekont='Federasyon', branch=seminar.branch)
            visa.startDate = date(int(seminar.year), 1, 1)
            visa.definition = CategoryItem.objects.get(forWhichClazz='VISA')
            visa.levelType = EnumFields.LEVELTYPE.VISA
            visa.status = HavaLevel.APPROVED
            visa.isActive = True
            visa.save()
            for referee in item.visa.all():
                if referee.branch == visa.branch:
                    referee.isActive = False
                    referee.save()
            item.visa.add(visa)
            item.save()
        seminar.status = VisaSeminar.APPROVED
        seminar.save()
    else:
        messages.warning(request, 'Seminer Daha Önce Onaylanmistir.')

    return redirect('sbs:update-visa-seminar', uuid=uuid)


@login_required
def addRefereeVisaSeminar(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    visa = VisaSeminar.objects.get(uuid=uuid)
    coa = []
    for item in visa.referee.all():
        coa.append(item.person.user.pk)
    referee = Referee.objects.exclude(person__user__id__in=coa)
    with transaction.atomic():
        if request.method == 'POST':
            athletes1 = request.POST.getlist('selected_options')
            if athletes1:
                for x in athletes1:
                    if not visa.referee.filter(person__user_id__in=x):
                        visa.referee.add(x)
                        visa.save()
            return redirect('sbs:update-visa-seminar', uuid=uuid)
    return render(request, 'TVGFBF/Referee/add-referee-visa-seminar.html', {'referees': referee})


@login_required
def addRefereeVisaSeminarApi(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():

            if request.method == 'POST' and request.is_ajax():
                list = request.POST.getlist('referee_list[]')
                visa = VisaSeminar.objects.get(uuid=request.POST['uuid'])
                for item in list:
                    if not visa.referee.filter(person__user_id__in=item):
                        visa.referee.add(item)
                        visa.save()

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def deleteRefereeVisaSeminar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                referee_uuid = request.POST['referee_uuid']
                competition_uuid = request.POST['competition_uuid']
                visa = VisaSeminar.objects.get(uuid=competition_uuid)
                visa.referee.remove(Referee.objects.get(uuid=referee_uuid))
                visa.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def deleteVisaSeminar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                obj = VisaSeminar.objects.get(uuid=uuid)
                obj.isDeleted = 1
                obj.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except VisaSeminar.DoesNotExist:
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def returnVisaSeminarApplication(request):
    perm = general_methods.control_access_referee(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    basvurularim = RefereeApplication.objects.none()
    referee = Referee.objects.get(person__user=user)
    if request.user.groups.filter(name='Hakem').exists():
        seminar = VisaSeminar.objects.filter(refereeApplication__referee__person__user=user).filter(
            forWhichClazz='REFEREE').distinct()
        basvurularim = RefereeApplication.objects.filter(referee__person__user=user)
    else:
        seminar = VisaSeminar.objects.filter(forWhichClazz='REFEREE')

    return render(request, 'TVGFBF/Referee/visa-seminar.html',
                  {'seminer': seminar, 'basvuru': basvurularim, 'user': user, 'referee': referee})


@login_required
def deleteRefereeApplicationVisaSeminar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                refereeApplication_uuid = request.POST['refereeApplication_uuid']
                seminer_uuid = request.POST['seminer_uuid']
                refereeApplication = RefereeApplication.objects.get(uuid=refereeApplication_uuid)
                refereeApplication.status = RefereeApplication.DENIED
                refereeApplication.save()

                seminer = VisaSeminar.objects.get(uuid=seminer_uuid)

                html_content = ''
                subject, from_email, to = 'THF Bilgi Sistemi', 'no-reply@halter.gov.tr', refereeApplication.referee.person.user.email
                html_content = '<h2>TÜRKİYE HALTER FEDERASYONU BİLGİ SİSTEMİ</h2>'
                html_content = '<p><strong>' + str(seminer.name) + '</strong> Seminer  başvurunuz reddedilmiştir.</p>'

                msg = EmailMultiAlternatives(subject, '', from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                log = str(seminer.name) + "    seminer basvusu reddedilmiştir    " + str(
                    refereeApplication.referee.person.user.get_full_name())
                log = general_methods.logwrite(request, request.user, log)

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def approvalRefereeApplicationVisaSeminar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                refereeApplication_uuid = request.POST['refereeApplication_uuid']
                seminer_uuid = request.POST['seminer_uuid']

                application = RefereeApplication.objects.get(uuid=refereeApplication_uuid)
                seminer = VisaSeminar.objects.get(uuid=seminer_uuid)
                seminer.referee.add(application.referee)
                seminer.save()
                application.status = RefereeApplication.APPROVED
                application.save()

                html_content = ''
                subject, from_email, to = 'THF Bilgi Sistemi', 'no-reply@halter.gov.tr', application.referee.person.user.email
                html_content = '<h2>TÜRKİYE HALTER FEDERASYONU BİLGİ SİSTEMİ</h2>'
                html_content = '<p><strong>' + str(seminer.name) + '</strong> Seminer  başvurunuz onaylanmıştır.</p>'

                msg = EmailMultiAlternatives(subject, '', from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                log = str(seminer.name) + "    seminer basvusu onaylanmıştır    " + str(
                    application.referee.person.user.get_full_name())
                log = general_methods.logwrite(request, request.user, log)
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def document(request, uuid):
    referee = Referee.objects.get(uuid=uuid)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="ProjeTakip.pdf"'
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.setTitle('Hakem Belge')

    logo = ImageReader(settings.MEDIA_ROOT + '/hakembelge.png')
    c.drawImage(logo, 0, 0, width=600, height=850, mask='auto')

    c.setFont("Times-Roman", 32)

    c.rotate(90)
    # change color
    # c.setFillColorRGB(0, 0, 0.77)
    # say hello (note after rotate the y coord ne
    c.drawString(270, -310, referee.person.user.get_full_name())

    c.showPage()

    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


@login_required
def referencedListReferee(request):  # Hakem başvuruları
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    referee = ReferenceReferee.objects.all().order_by('status')
    return render(request, 'TVGFBF/Referee/referenceListReferee.html', {'referees': referee,'urls':urls,'current_url':current_url,'url_name':url_name})


@login_required
def refenceapprovalReferee(request):  # Hakem basvuru onayla
    # perm = general_methods.control_access(request)
    #
    # if not perm:
    #     logout(request)
    #     return redirect('accounts:login')
    reference = ReferenceReferee.objects.get(uuid=request.POST['uuid'])
    with transaction.atomic():
        if request.method == 'POST' and request.is_ajax():
            try:
                with transaction.atomic():

                    if reference.status == ReferenceReferee.WAITED:
                        user = User()
                        user.username = reference.email
                        user.first_name = reference.first_name
                        user.last_name = reference.last_name
                        user.email = reference.email
                        password = User.objects.make_random_password()
                        user.set_password(password)
                        user.is_active = True
                        user.save()
                        group = Group.objects.get(name='Hakem')
                        user.groups.add(group)

                        user.save()

                        person = Person()
                        person.tc = reference.tc
                        person.motherName = reference.motherName
                        person.fatherName = reference.fatherName
                        person.profileImage = reference.profileImage
                        person.birthDate = reference.birthDate
                        person.bloodType = reference.bloodType
                        person.birthplace = reference.birthplace
                        if reference.gender == 'Erkek':
                            person.gender = Person.MALE
                        else:
                            person.gender = Person.FEMALE
                        person.save()
                        person.user = user
                        person.save()
                        communication = Communication()
                        communication.postalCode = reference.postalCode
                        communication.phoneNumber = reference.phoneNumber
                        communication.phoneNumber2 = reference.phoneNumber2
                        communication.address = reference.address
                        communication.city = reference.city
                        communication.country = reference.country
                        communication.save()

                        judge = Referee(person=person, communication=communication)
                        # judge.iban = reference.iban
                        judge.save()

                        grade = HavaLevel(definition=reference.kademe_definition,
                                          startDate=reference.kademe_startDate,
                                          )
                        grade.levelType = EnumFields.LEVELTYPE.GRADE
                        grade.status = HavaLevel.APPROVED
                        grade.isActive = True
                        grade.save()

                        judge.grades.add(grade)
                        judge.save()

                        reference.status = ReferenceReferee.APPROVED
                        reference.save()

                        messages.success(request, 'Hakem Başarıyla Eklenmiştir')

                        fdk = Forgot(user=user, status=False)
                        fdk.save()
                        print(fdk)

                        # html_content = ''
                        # subject, from_email, to = 'Bilgi Sistemi Kullanıcı Bilgileri', 'kayit@tvgfbf.gov.tr', user.email
                        # html_content = '<h2>TÜRKİYE VÜCUT GELİŞTİRME FİTNESS VE BİLEK GÜREŞİ FEDERASYONU BİLGİ SİSTEMİ</h2>'
                        # html_content = html_content + '<p>Başvurunuz Onaylanmıştır.</p>'
                        # html_content = html_content + '<p><strong>Kullanıcı Adınız :' + str(
                        #     fdk.user.username) + '</strong></p>'
                        # html_content = html_content + '<p><strong>Şifreniz :' + str(password) + '</strong></p>'
                        # html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="https://sbs.tvgfbf.gov.tr/">https://sbs.tvgfbf.gov.tr/</p></a>'
                        # msg = EmailMultiAlternatives(subject, '', from_email, [to])
                        # msg.attach_alternative(html_content, "text/html")
                        # msg.send()

                        log = str(user.get_full_name()) + " Hakem basvurusu onaylandi"
                        log = general_methods.logwrite(request, request.user, log)


                    else:
                        reference.status = reference.APPROVED
                        reference.save()
                        messages.success(request, 'Hakem daha önce onaylanmıştır.')

                    return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            except Referee.DoesNotExist:
                return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

        else:
            return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def referenceUpdateReferee(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    refere = ReferenceReferee.objects.get(uuid=uuid)
    refere_form = PreRefereeForm(request.POST or None, request.FILES or None, instance=refere,
                                 initial={'kademe_definition': refere.kademe_definition})

    try:
        with transaction.atomic():
            if request.method == 'POST':
                # mail = request.POST.get('email')
                # if mail != refere.email:
                #
                #     if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                #             email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
                #         email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
                #         email=mail):
                #         messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
                #         return render(request, 'TVGFBF/Referee/updateReferenceReferee.html',
                #                       {'preRegistrationform': refere_form})

                # tc = request.POST.get('tc')
                # if tc != refere.tc:
                #
                #     if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                #             tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
                #         tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
                #         messages.warning(request, 'Tc kimlik numarasi sisteme kayıtlıdır. ')
                #         return render(request, 'TVGFBF/Referee/updateReferenceReferee.html',
                #                       {'preRegistrationform': refere_form})

                name = request.POST.get('first_name')
                surname = request.POST.get('last_name')
                year = request.POST.get('birthDate')
                year = year.split('/')

                # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
                # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
                #     messages.warning(request, 'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
                #     return render(request, 'TVGFBF/Referee/updateReferenceReferee.html',
                #                   {'preRegistrationform': refere_form})

                if refere_form.is_valid():
                    refere_form.save()
                    messages.success(request, 'Hakem Başvurusu Güncellendi')
                    return redirect('sbs:referencedListReferee')
                else:
                    messages.warning(request, 'Alanları Kontrol Ediniz')
        return render(request, 'TVGFBF/Referee/updateReferenceReferee.html', {'preRegistrationform': refere_form})
    except ReferenceReferee.DoesNotExist:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def refencedeleteReferee(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    with transaction.atomic():
        if request.method == 'POST' and request.is_ajax():
            try:
                obj = ReferenceReferee.objects.get(uuid=request.POST['uuid'])
                obj.status = ReferenceReferee.DENIED
                obj.save()

                # html_content = ''
                # subject, from_email, to = 'Bilgi Sistemi Kullanıcı Bilgileri', 'kayit@tvgfbf.gov.tr', obj.email
                # html_content = '<h2>TÜRKİYE VÜCUT GELİŞTİRME FİTNESS VE BİLEK GÜREŞİ FEDERASYONU BİLGİ SİSTEMİ</h2>'
                # html_content = html_content + '<p>Başvurunuz Reddedilmiştir.</p>'
                # msg = EmailMultiAlternatives(subject, '', from_email, [to])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()

                log = str(obj.first_name) + " " + str(obj.last_name) + "     Hakem basvurusu reddedildi"
                log = general_methods.logwrite(request, request.user, log)

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            except Referee.DoesNotExist:
                return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

        else:
            return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
