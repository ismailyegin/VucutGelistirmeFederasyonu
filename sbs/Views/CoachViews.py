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
from django.utils import timezone
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from zeep import Client

from accounts.models import Forgot
from sbs.Forms.CategoryItemForm import CategoryItemForm
from sbs.Forms.havaspor.GradeFormCoach import GradeFormCoach
from sbs.Forms.havaspor.CoachSearchForm import CoachSearchForm
from sbs.Forms.havaspor.CommunicationForm import CommunicationForm
from sbs.Forms.havaspor.HavaUserForm import HavaUserForm
from sbs.Forms.havaspor.PersonForm import PersonForm
from sbs.Forms.havaspor.SearchClupForm import SearchClupForm
from sbs.Forms.havaspor.VisaForm import VisaForm
from sbs.Forms.havaspor.VisaSeminarForm import VisaSeminarForm
from sbs.models.ekabis.CategoryItem import CategoryItem
from sbs.models.ekabis.Competition import Competition
from sbs.models.tvfbf.CoachApplication import CoachApplication
from sbs.models.tvfbf.HavaLevel import HavaLevel
from sbs.models.ekabis.Logs import Logs
from sbs.models.ekabis.Permission import Permission
from sbs.models.ekabis.EnumFields import EnumFields
from sbs.models.ekabis.Person import Person
from sbs.models.ekabis.Communication import Communication
from sbs.models.tvfbf.Coach import Coach
from sbs.models.tvfbf.Club import Club
from sbs.models.tvfbf.SportClubUser import SportClubUser
from sbs.models.tvfbf.VisaSeminar import VisaSeminar
from sbs.services import general_methods
from sbs.services.general_methods import get_client_ip
from sbs.services.services import last_urls


@login_required
def return_coachs(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    coachs = Coach.objects.none()
    clubs = Club.objects.all()
    user_form = CoachSearchForm()
    searchClupForm = SearchClupForm()

    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    if request.method == 'POST':
        user_form = CoachSearchForm(request.POST)
        searchClupForm = SearchClupForm(request.POST)
        branch = request.POST.get('branch')
        # grade = request.POST.get('definition')
        # visa = request.POST.get('visa')
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        email = request.POST.get('email')

        if not (firstName or lastName or email or branch):
            if user.groups.filter(name='KulupUye'):
                sc_user = SportClubUser.objects.get(user=user)
                clubsPk = []
                clubs = Club.objects.filter(clubUser=sc_user)
                for club in clubs:
                    clubsPk.append(club.pk)
                coachs = Coach.objects.filter(sportsclub__in=clubsPk).filter(isDeleted=0).distinct()
            elif user.groups.filter(name__in=['Yonetim', 'Admin']):
                coachs = Coach.objects.filter(isDeleted=0)
        else:
            query = Q()
            if lastName:
                query &= Q(person__user__last_name__icontains=lastName.title())
            if firstName:
                query &= Q(person__user__first_name__icontains=firstName.title())
            if email:
                query &= Q(person__user__email__icontains=email)
            if branch:
                query &= Q(branch__title=branch)
            # if grade:
            #     query &= Q(grades__definition__name=grade, grades__status='Onaylandı')
            # if visa == 'VISA':
            #     query &= Q(visa__startDate__year=timezone.now().year, visa__status='Onaylandı')

            if user.groups.filter(name='KulupUye'):
                sc_user = SportClubUser.objects.get(user=user)
                clubsPk = []
                clubs = Club.objects.filter(clubUser=sc_user)
                for club in clubs:
                    clubsPk.append(club.pk)
                coachs = Coach.objects.filter(query).filter(sportsclub__in=clubsPk).filter(isDeleted=0).distinct()
            elif user.groups.filter(name__in=['Yonetim', 'Admin']):
                coachs = Coach.objects.filter(query).filter(isDeleted=0)
            # if visa == 'NONE':
            #     coachs = coachs.exclude(visa__startDate__year=timezone.now().year, visa__status='Onaylandı')
    return render(request, '_HavaSpor/Coach/coachs.html',
                  {'coachs': coachs, 'user_form': user_form, 'branch': searchClupForm, 'clubs': clubs, })


@login_required
def return_add_coach(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user_form = HavaUserForm()
    person_form = PersonForm()
    communication_form = CommunicationForm()

    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    if request.method == 'POST':

        user_form = HavaUserForm(request.POST)
        person_form = PersonForm(request.POST, request.FILES)
        communication_form = CommunicationForm(request.POST)
        mail = request.POST.get('email')

        # if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
        #         email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
        #     email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
        #     email=mail):
        #     messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
        #     return render(request, '_HavaSpor/Coach/add-coach.html',
        #                   {'user_form': user_form, 'person_form': person_form,
        #                    'communication_form': communication_form, 'urls': urls, 'current_url': current_url,
        #                    'url_name': url_name, })

        tc = request.POST.get('tc')
        # if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
        #         tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
        #     tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
        #     messages.warning(request, 'Tc kimlik numarasi sisteme kayıtlıdır. ')
        #     return render(request, '_HavaSpor/Coach/add-coach.html',
        #                   {'user_form': user_form, 'person_form': person_form,
        #                    'communication_form': communication_form, 'urls': urls, 'current_url': current_url,
        #                    'url_name': url_name, })

        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        year = request.POST.get('birthDate')
        year = year.split('/')

        # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
        # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
        #     messages.warning(request, 'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
        #     return render(request, '_HavaSpor/Coach/add-coach.html',
        #                   {'user_form': user_form, 'person_form': person_form,
        #                    'communication_form': communication_form, 'urls': urls, 'current_url': current_url,
        #                    'url_name': url_name, })

        if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid():
            user = User()
            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            group = Group.objects.get(name='Antrenör')
            password = User.objects.make_random_password()
            user.set_password(password)
            user.is_active = True
            user.save()
            user.groups.add(group)

            user.save()

            log = str(user.get_full_name()) + " Antrenoru ekledi"
            log = general_methods.logwrite(request, request.user, log)

            person = person_form.save(commit=False)
            iban = request.POST.get("iban")
            person.iban = iban
            person.user = user
            communication = communication_form.save(commit=False)
            person.save()
            communication.save()

            coach = Coach(person=person, communication=communication)
            coach.save()
            # antroner kaydından sonra mail gönderilmeyecek

            # subject, from_email, to = 'Halter - Antrenör Bilgi Sistemi Kullanıcı Giriş Bilgileri', 'no-reply@twf.gov.tr', user.email
            # text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
            # html_content = '<p> <strong>Site adresi: </strong> <a href="http://sbs.twf.gov.tr:81/"></a>sbs.twf.gov.tr:81</p>'
            # html_content = html_content + '<p><strong>Kullanıcı Adı:  </strong>' + user.username + '</p>'
            # html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()

            fdk = Forgot(user=user, status=False)
            fdk.save()

            html_content = ''
            subject, from_email, to = 'Bilgi Sistemi Kullanıcı Bilgileri', 'no-reply@halter.gov.tr', user.email
            html_content = '<h2>TÜRKİYE HALTER FEDERASYONU BİLGİ SİSTEMİ</h2>'
            html_content = html_content + '<p><strong>Kullanıcı Adınız :' + str(fdk.user.username) + '</strong></p>'
            html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="https://sbs.halter.gov.tr:9443/newpassword?query=' + str(
                fdk.uuid) + '">https://sbs.halter.gov.tr:9443/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'
            msg = EmailMultiAlternatives(subject, '', from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, 'Antrenör Başarıyla Kayıt Edilmiştir.')

            return redirect('sbs:return_coachs')

        else:

            for x in user_form.errors.as_data():
                messages.warning(request, user_form.errors[x][0])

    return render(request, '_HavaSpor/Coach/add-coach.html',
                  {'user_form': user_form, 'person_form': person_form,
                   'communication_form': communication_form, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name, })


@login_required
def coachUpdate(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    coach = Coach.objects.get(uuid=uuid)

    grade_form = coach.grades.filter(isDeleted=0)
    visa_form = coach.visa.filter(isDeleted=0)
    user = User.objects.get(pk=coach.person.user.pk)
    person = Person.objects.get(pk=coach.person.pk)
    communication = Communication.objects.get(pk=coach.communication.pk)
    user_form = HavaUserForm(request.POST or None, instance=user)
    person_form = PersonForm(request.POST or None, request.FILES or None, instance=person)
    communication_form = CommunicationForm(request.POST or None, instance=communication)

    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    if request.method == 'POST':
        user = User.objects.get(pk=coach.person.user.pk)
        user_form = HavaUserForm(request.POST or None, instance=user)
        person_form = PersonForm(request.POST, request.FILES, instance=person)
        communication_form = CommunicationForm(request.POST or None, instance=communication)

        mail = request.POST.get('email')
        # if mail != coach.user.email:
        #
        #     if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
        #             email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
        #         email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
        #         email=mail):
        #         messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
        #         return render(request, '_HavaSpor/Coach/update-coach.html',
        #                       {'user_form': user_form, 'communication_form': communication_form,
        #                        'person_form': person_form, 'grades_form': grade_form, 'coach': coach.pk,
        #                        'personCoach': person, 'visa_form': visa_form, 'urls': urls, 'current_url': current_url,
        #                    'url_name': url_name, })

        tc = request.POST.get('tc')
        # if tc != coach.person.tc:
        #     if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
        #             tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
        #         tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
        #         messages.warning(request, 'Tc kimlik numarasi sisteme kayıtlıdır. ')
        #         return render(request, '_HavaSpor/Coach/update-coach.html',
        #                       {'user_form': user_form, 'communication_form': communication_form,
        #                        'person_form': person_form, 'grades_form': grade_form, 'coach': coach.pk,
        #                        'personCoach': person, 'visa_form': visa_form, 'urls': urls, 'current_url': current_url,
        #                    'url_name': url_name, })

        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        year = request.POST.get('birthDate')
        year = year.split('/')

        # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
        # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
        #     messages.warning(request, 'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
        #     return render(request, '_HavaSpor/Coach/update-coach.html',
        #                   {'user_form': user_form, 'communication_form': communication_form,
        #                    'person_form': person_form, 'grades_form': grade_form, 'coach': coach.pk,
        #                    'personCoach': person, 'visa_form': visa_form, 'urls': urls, 'current_url': current_url,
        #                    'url_name': url_name, })

        if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid():

            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            user.save()

            user = user_form.save(commit=False)
            user.username = user_form.cleaned_data['email']
            user.save()

            log = str(user.get_full_name()) + " Antrenor güncelledi"
            log = general_methods.logwrite(request, request.user, log)

            person = person_form.save(commit=False)
            iban = request.POST.get("iban")
            person.iban = iban
            person.save()
            communication_form.save()

            messages.success(request, 'Antrenör Başarıyla Güncellendi')
            return redirect('sbs:return_coachs')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, '_HavaSpor/Coach/update-coach.html',
                  {'user_form': user_form, 'communication_form': communication_form,
                   'person_form': person_form, 'grades_form': grade_form, 'coach': coach,
                   'personCoach': person, 'visa_form': visa_form, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name, })


@login_required
def delete_coach(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']

                obj = Coach.objects.get(uuid=uuid)
                data_as_json_pre = serializers.serialize('json', Coach.objects.filter(uuid=uuid))

                obj.isDeleted = True
                obj.save()
                log = "Antrenör Sil"
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
def add_coach_referee(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    coach = Coach.objects.get(uuid=uuid)
    grade_form = GradeFormCoach()

    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    if request.method == 'POST':
        grade_form = GradeFormCoach(request.POST, request.FILES)

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
            for item in coach.grades.all():
                if item.branch == grade.branch:
                    item.isActive = False
                    item.save()

            coach.grades.add(grade)
            coach.save()

            log = str(coach.person.user.get_full_name()) + " Kademe eklendi"
            log = general_methods.logwrite(request, request.user, log)

            messages.success(request, 'Kademe Başarıyla Eklenmiştir.')
            return redirect('sbs:update_coach', uuid=uuid)

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    grade_form.fields['definition'].queryset = CategoryItem.objects.filter(forWhichClazz='COACH_GRADE')
    return render(request, '_HavaSpor/Coach/add-grade-coach.html',
                  {'grade_form': grade_form, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name, })


@login_required
def grade_approval(request, grade_uuid, coach_uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade = HavaLevel.objects.get(uuid=grade_uuid)
    coach = Coach.objects.get(uuid=coach_uuid)
    try:
        for item in coach.grades.all():
            if item.branch == grade.branch:
                item.isActive = False
                item.save()
        grade.status = HavaLevel.APPROVED
        grade.isActive = True
        grade.save()

        log = str(coach.person.user.get_full_name()) + " Kademe onaylandi"
        log = general_methods.logwrite(request, request.user, log)

        messages.success(request, 'Kademe   Onaylanmıştır')
    except:
        messages.warning(request, 'Lütfen yeniden deneyiniz.')
    return redirect('sbs:update_coach', uuid=coach_uuid)


@login_required
def grade_reject(request, grade_uuid, coach_uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade = HavaLevel.objects.get(uuid=grade_uuid)
    grade.status = HavaLevel.DENIED
    grade.save()

    coach = Coach.objects.get(uuid=coach_uuid)
    log = str(coach.person.user.get_full_name()) + " Kademe reddedildi"
    log = general_methods.logwrite(request, request.user, log)

    messages.success(request, 'Kademe Reddedilmiştir')
    return redirect('sbs:update_coach', uuid=coach_uuid)


@login_required
def update_grade(request, grade_uuid, coach_uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade = HavaLevel.objects.get(uuid=grade_uuid)
    coach = Coach.objects.get(uuid=coach_uuid)
    grade_form = GradeFormCoach(request.POST or None, request.FILES or None, instance=grade,
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

                log = str(coach.person.user.get_full_name()) + " Kademe guncellendi"
                log = general_methods.logwrite(request, request.user, log)
            messages.success(request, 'Kademe Başarılı bir şekilde güncellenmiştir.')
            return redirect('sbs:update_coach', uuid=coach_uuid)

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, '_HavaSpor/Coach/update-grade-coach.html',
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
                coach_uuid = request.POST['coach_uuid']

                obj = HavaLevel.objects.get(uuid=grade_uuid)
                coach = Coach.objects.get(uuid=coach_uuid)

                data_as_json_pre = serializers.serialize('json', Coach.objects.filter(uuid=coach_uuid))

                obj.isDeleted = True
                obj.save()
                log = "Antrenör Kademe Sil"
                logs = Logs(user=request.user, subject=log, ip=get_client_ip(request),
                            previousData=data_as_json_pre)
                logs.save()

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


def add_visa_coach(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    coach = Coach.objects.get(uuid=uuid)
    visa_form = VisaForm()
    category_item_form = CategoryItemForm()
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    if request.method == 'POST':
        visa_form = VisaForm(request.POST, request.FILES)
        category_item_form = CategoryItemForm(request.POST, request.FILES)

        try:
            if visa_form.is_valid():

                visa = HavaLevel(dekont=visa_form.cleaned_data['dekont'], branch=visa_form.cleaned_data['branch'])
                visa.startDate = visa_form.cleaned_data['startDate']

                visa.definition = CategoryItem.objects.get(forWhichClazz='VISA_COACH')
                visa.levelType = EnumFields.LEVELTYPE.VISA
                visa.status = HavaLevel.WAITED
                for item in coach.visa.all():
                    if item.branch == visa.branch:
                        item.isActive = False
                        item.save()
                visa.isActive = True

                visa.save()
                coach.visa.add(visa)
                coach.save()

                log = str(coach.person.user.get_full_name()) + " Antrenör  vize eklendi"
                log = general_methods.logwrite(request, request.user, log)

                messages.success(request, 'Vize Başarıyla Eklenmiştir.')
                return redirect('sbs:update_coach', uuid=uuid)
        except:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, '_HavaSpor/Coach/add-visa-coach.html',
                  {'visa_form': visa_form, 'category_item_form': category_item_form, 'urls': urls,
                   'current_url': current_url,
                   'url_name': url_name, })


@login_required
def visa_approval(request, visa_uuid, coach_uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    visa = HavaLevel.objects.get(uuid=visa_uuid)
    visa.status = HavaLevel.APPROVED
    visa.save()
    coach = Coach.objects.get(uuid=coach_uuid)
    log = str(coach.person.user.get_full_name()) + " vize onaylandi"
    log = general_methods.logwrite(request, request.user, log)

    messages.success(request, 'Vize onaylanmıştır.')
    return redirect('sbs:update_coach', uuid=coach_uuid)


@login_required
def visa_reject(request, visa_uuid, coach_uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    visa = HavaLevel.objects.get(uuid=visa_uuid)
    visa.status = HavaLevel.DENIED
    visa.save()
    coach = Coach.objects.get(uuid=coach_uuid)
    log = str(coach.person.user.get_full_name()) + " vize reddedildi"
    log = general_methods.logwrite(request, request.user, log)

    messages.warning(request, 'Vize Reddedilmiştir.')
    return redirect('sbs:update_coach', uuid=coach_uuid)


@login_required
def visa_update(request, visa_uuid, coach_uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    visa = HavaLevel.objects.get(uuid=visa_uuid)
    coach = Coach.objects.get(uuid=coach_uuid)
    visa_form = VisaForm(request.POST or None, request.FILES or None, instance=visa)

    if request.method == 'POST':
        if visa_form.is_valid():
            visa_form.save()
            if visa.status != HavaLevel.APPROVED:
                visa.status = HavaLevel.WAITED
                visa.save()

                log = str(coach.person.user.get_full_name()) + " antrenör  vize güncellendi"
                log = general_methods.logwrite(request, request.user, log)

                messages.success(request, 'Vize Başarıyla Güncellenmiştir.')
                return redirect('sbs:update_coach', uuid=coach_uuid)
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, '_HavaSpor/Coach/update-visa-coach.html',
                  {'visa_form': visa_form})


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
                coach_uuid = request.POST['coach_uuid']

                obj = HavaLevel.objects.get(uuid=visa_uuid)
                coach = Coach.objects.get(uuid=coach_uuid)

                data_as_json_pre = serializers.serialize('json', Coach.objects.filter(uuid=coach_uuid))

                obj.isDeleted = True
                obj.save()
                log = "Antrenör Vize Sil"
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
def return_grade(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    category_item_form = CategoryItemForm()

    if request.method == 'POST':

        category_item_form = CategoryItemForm(request.POST)

        if category_item_form.is_valid():

            categoryItem = CategoryItem(name=category_item_form.cleaned_data['name'])
            categoryItem.forWhichClazz = "COACH_GRADE"
            categoryItem.save()

            return redirect('sbs:return_grade')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')
    categoryitem = CategoryItem.objects.filter(forWhichClazz="COACH_GRADE", isDeleted=0)
    return render(request, '_HavaSpor/Coach/grades.html',
                  {'category_item_form': category_item_form, 'categoryitem': categoryitem})


@login_required
def gradeUpdate(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    categoryItem = CategoryItem.objects.get(uuid=uuid)
    category_item_form = CategoryItemForm(request.POST or None, instance=categoryItem)
    if request.method == 'POST':
        if category_item_form.is_valid():
            category = category_item_form.save(request, commit=False)
            category.save()
            messages.success(request, 'Başarıyla Güncellendi')
            return redirect('sbs:return_grade')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, '_HavaSpor/Coach/update-grade.html',
                  {'category_item_form': category_item_form})


def gradeDelete(request):
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

    coa = []
    for item in CategoryItem.objects.filter(forWhichClazz='COACH_GRADE'):
        coa.append(item.pk)
    grade = HavaLevel.objects.filter(definition_id__in=coa, levelType=EnumFields.LEVELTYPE.GRADE,
                                     isDeleted=0).distinct()

    return render(request, '_HavaSpor/Coach/coach-grade-list.html',
                  {'coachGrades': grade})



@login_required
def gradeListApproval(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade = HavaLevel.objects.get(uuid=uuid)
    coach = grade.CoachGrades.first()
    try:
        for item in coach.grades.all():
            if item.branch == grade.branch:
                item.isActive = False
                item.save()
        grade.status = HavaLevel.APPROVED
        grade.isActive = True
        grade.save()
        messages.success(request, 'Kademe   Onaylanmıştır')
    except:
        messages.warning(request, 'Lütfen yeniden deneyiniz.')

    return redirect('sbs:coach_grade_list')


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
    return redirect('sbs:coach_grade_list')


def gradeListApprovalAll(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    coa = []
    for item in CategoryItem.objects.filter(forWhichClazz='COACH_GRADE'):
        coa.append(item.pk)
    grades = HavaLevel.objects.filter(definition_id__in=coa, levelType=EnumFields.LEVELTYPE.GRADE, status="Beklemede")

    for grade in grades:
        coach = grade.CoachGrades.first()
        try:
            for item in coach.grades.all():
                if item.branch == grade.branch:
                    item.isActive = False
                    item.save()
            grade.status = HavaLevel.APPROVED
            grade.isActive = True
            grade.save()
            messages.success(request, 'Beklemede olan Kademeler Onaylanmıştır')
        except:
            messages.warning(request, 'Lütfen yeniden deneyiniz.')

    return redirect('sbs:coach_grade_list')


@login_required
def gradeListRejectAll(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    coa = []
    for item in CategoryItem.objects.filter(forWhichClazz='COACH_GRADE'):
        coa.append(item.pk)
    grades = HavaLevel.objects.filter(definition_id__in=coa, levelType=EnumFields.LEVELTYPE.GRADE, status="Beklemede")
    for grade in grades:
        grade.status = HavaLevel.DENIED
        grade.save()
    messages.success(request, 'Beklemede olan kademeler   Onaylanmıştır')
    return redirect('sbs:coach_grade_list')


@login_required
def visaList(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    coa = []
    for item in CategoryItem.objects.filter(forWhichClazz='VISA_COACH'):
        coa.append(item.pk)
    visa = HavaLevel.objects.filter(definition_id__in=coa, levelType=EnumFields.VISA, isDeleted=0).distinct()
    return render(request, '_HavaSpor/Coach/coach-visa-list.html',
                  {'coachvisas': visa})



@login_required
def visaListApproval(request, uuid):
    try:
        perm = general_methods.control_access(request)

        if not perm:
            logout(request)
            return redirect('accounts:login')
        visa = HavaLevel.objects.get(uuid=uuid)
        visa.status = HavaLevel.APPROVED
        coach = visa.CoachVisa.first()
        for item in coach.visa.all():
            if item.branch == visa.branch:
                item.isActive = False
                item.save()
        visa.isActive = True
        visa.save()
        messages.success(request, 'Vize Onaylanmıştır.')
    except:
        messages.warning(request, 'Yeniden deneyiniz.')

    return redirect('sbs:coach_visa_list')


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
    return redirect('sbs:coach_visa_list')


@login_required
def returnVisaSeminarApplication(request):
    perm = general_methods.control_access_klup(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    basvurularim = CoachApplication.objects.none()
    coach = Coach.objects.get(person__user=user)
    if request.user.groups.filter(name='Antrenör').exists():
        seminar = VisaSeminar.objects.filter(coachApplication__coach__user=user).filter(
            forWhichClazz='COACH').distinct()
        basvurularim = CoachApplication.objects.filter(coach__user=user)

    else:
        seminar = VisaSeminar.objects.filter(forWhichClazz='COACH')

    return render(request, '_HavaSpor/Coach/visa-seminar.html', {'seminer': seminar, 'basvuru': basvurularim, 'coach': coach})


@login_required
def returnVisaSeminar(request):
    perm = general_methods.control_access_klup(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user

    seminar = VisaSeminar.objects.filter(forWhichClazz='COACH', isDeleted=0)

    if request.method == 'POST':
        if user.groups.filter(name='Antrenör').exists():
            vizeSeminer = VisaSeminar.objects.get(pk=request.POST.get('pk'))
            coach = Coach.objects.get(user=request.user)
            try:
                if request.FILES['file']:
                    document = request.FILES['file']
                    data = CoachApplication()
                    data.dekont = document
                    data.coach = coach
                    data.save()
                    vizeSeminer.coachApplication.add(data)
                    vizeSeminer.save()

                    messages.success(request, 'Vize Seminerine Başvuru  gerçekleşmiştir.')
                    return redirect('sbs:return-coach-visa-seminar-application')


            except:
                messages.warning(request, 'Lütfen yeniden deneyiniz')

    return render(request, '_HavaSpor/Coach/coach-visa-seminar.html', {'competitions': seminar})



@login_required
def addVisaSeminar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    visaSeminar = VisaSeminarForm()
    if request.method == 'POST':
        visaSeminar = VisaSeminarForm(request.POST)
        if visaSeminar.is_valid():

            visa = visaSeminar.save()
            visa.forWhichClazz = 'COACH'
            visa.save()
            messages.success(request, 'Vize Semineri Başari  Kaydedilmiştir.')

            return redirect('sbs:coach-visa-seminar')
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, '_HavaSpor/Coach/add-visa-seminar-coach.html',
                  {'competition_form': visaSeminar})


@login_required
def updateVisaSeminar(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    seminar = VisaSeminar.objects.get(uuid=uuid)
    coach = seminar.coach.all()
    competition_form = VisaSeminarForm(request.POST or None, instance=seminar)
    if request.method == 'POST':
        if competition_form.is_valid():
            competition_form.save()
            messages.success(request, 'Vize Seminer Başarıyla Güncellenmiştir.')

            return redirect('sbs:coach-visa-seminar')
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, '_HavaSpor/Coach/update-coach-visa-seminar.html',
                  {'competition_form': competition_form, 'competition': seminar, 'coachs': coach})


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
    except Competition.DoesNotExist:
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def visaSeminarApproval(request, uuid):
    seminar = VisaSeminar.objects.get(uuid=uuid)

    if seminar.status == VisaSeminar.WAITED:

        for item in seminar.coach.all():
            visa = HavaLevel(dekont='Federasyon', branch=seminar.branch)
            visa.startDate = date(int(seminar.year), 1, 1)
            visa.definition = CategoryItem.objects.get(forWhichClazz='VISA')
            visa.levelType = EnumFields.LEVELTYPE.VISA
            visa.status = HavaLevel.APPROVED
            visa.isActive = True
            visa.save()
            for coach in item.visa.all():
                if coach.branch == visa.branch:
                    coach.isActive = False
                    coach.save()
            item.visa.add(visa)
            item.save()
        seminar.status = VisaSeminar.APPROVED
        seminar.save()
    else:
        messages.warning(request, 'Seminer Daha Önce Onaylanmistir.')

    return redirect('sbs:update-coach-visa-seminar', uuid=uuid)



@login_required
def addCoachVisaSeminar(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    visa = VisaSeminar.objects.get(uuid=uuid)
    coa = []
    for item in visa.coach.all():
        coa.append(item.person.user.pk)
    coach = Coach.objects.exclude(person__user__id__in=coa)

    if request.method == 'POST':
        athletes1 = request.POST.getlist('selected_options')
        if athletes1:
            for x in athletes1:
                if not visa.coach.filter(person__user_id__in=x):
                    visa.coach.add(x)
                    visa.save()
        return redirect('sbs:update-coach-visa-seminar', uuid=uuid)
    return render(request, '_HavaSpor/Coach/add-coach-visa-seminar.html', {'coachs': coach})


@login_required
def deleteCoachVisaSeminar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                coach_uuid = request.POST['coach_uuid']
                competition_uuid = request.POST['competition_uuid']
                visa = VisaSeminar.objects.get(uuid=competition_uuid)
                visa.coach.remove(Coach.objects.get(uuid=coach_uuid))
                visa.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def deleteCoachApplicationVisaSeminar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                coachApplication_uuid = request.POST['coachApplication_uuid']
                seminer_uuid = request.POST['seminer_uuid']
                coachApplication = CoachApplication.objects.get(uuid=coachApplication_uuid)
                coachApplication.status = CoachApplication.DENIED
                coachApplication.save()

                seminer = VisaSeminar.objects.get(uuid=seminer_uuid)

                html_content = ''
                subject, from_email, to = 'THF Bilgi Sistemi', 'no-reply@halter.gov.tr', coachApplication.coach.person.user.email
                html_content = '<h2>TÜRKİYE HALTER FEDERASYONU BİLGİ SİSTEMİ</h2>'
                html_content = '<p><strong>' + str(seminer.name) + '</strong> Seminer  başvurunuz reddedilmiştir.</p>'

                msg = EmailMultiAlternatives(subject, '', from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                log = str(seminer.name) + "    seminer basvusu reddedilmiştir    " + str(
                    coachApplication.coach.person.user.get_full_name())
                log = general_methods.logwrite(request, request.user, log)

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def approvalCoachApplicationVisaSeminar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                coachApplication_uuid = request.POST['coachApplication_uuid']
                seminer_uuid = request.POST['seminer_uuid']

                coachApplication = CoachApplication.objects.get(uuid=coachApplication_uuid)
                seminer = VisaSeminar.objects.get(uuid=seminer_uuid)
                seminer.coach.add(coachApplication.coach)
                seminer.save()
                coachApplication.status = CoachApplication.APPROVED
                coachApplication.save()

                html_content = ''
                subject, from_email, to = 'THF Bilgi Sistemi', 'no-reply@halter.gov.tr', coachApplication.coach.person.user.email
                html_content = '<h2>TÜRKİYE HALTER FEDERASYONU BİLGİ SİSTEMİ</h2>'
                html_content = '<p><strong>' + str(seminer.name) + '</strong> Seminer  başvurunuz onaylanmıştır.</p>'

                msg = EmailMultiAlternatives(subject, '', from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                log = str(seminer.name) + "    seminer basvusu onaylanmıştır    " + str(
                    coachApplication.coach.person.user.get_full_name())
                log = general_methods.logwrite(request, request.user, log)
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})




@login_required
def document(request, uuid):
    coach = Coach.objects.get(uuid=uuid)

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
    c.drawString(270, -310, coach.person.user.get_full_name())

    c.showPage()

    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
