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
from django.utils import timezone
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from zeep import Client

from accounts.models import Forgot
from oxiterp.settings.base import EMAIL_HOST_USER
from sbs.Forms.CategoryItemForm import CategoryItemForm
from sbs.Forms.havaspor.GradeFormCoach import GradeFormCoach
from sbs.Forms.havaspor.CoachSearchForm import CoachSearchForm
from sbs.Forms.havaspor.CommunicationForm import CommunicationForm
from sbs.Forms.havaspor.HavaUserForm import HavaUserForm
from sbs.Forms.havaspor.PersonForm import PersonForm
from sbs.Forms.havaspor.ReferenceCoachForm import RefereeCoachForm
from sbs.Forms.havaspor.SearchClupForm import SearchClupForm
from sbs.Forms.havaspor.VisaForm import VisaForm
from sbs.Forms.havaspor.VisaSeminarForm import VisaSeminarForm
from sbs.models import Branch, City, Country, PreRegistration
from sbs.models.ekabis.CategoryItem import CategoryItem
from sbs.models.tvfbf.CoachApplication import CoachApplication
from sbs.models.tvfbf.HavaLevel import HavaLevel
from sbs.models.ekabis.Logs import Logs
from sbs.models.ekabis.Permission import Permission
from sbs.models.ekabis.EnumFields import EnumFields
from sbs.models.ekabis.Person import Person
from sbs.models.ekabis.Communication import Communication
from sbs.models.tvfbf.Coach import Coach
from sbs.models.tvfbf.Club import Club
from sbs.models.tvfbf.ReferenceCoach import ReferenceCoach
from sbs.models.tvfbf.ReferenceReferee import ReferenceReferee
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

    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    current_date = datetime.date.today()
    branches = Branch.objects.all()
    cities = City.objects.all()

    return render(request, 'TVGFBF/Coach/coachs.html',
                  {'current_date': current_date, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name, 'branches': branches, 'cities': cities, })


@login_required
def return_coach_search(request):
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
    current_date = datetime.date.today()

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
            elif user.groups.filter(name='Admin'):
                return redirect('sbs:return_coachs')
        else:
            query = Q()
            if lastName:
                query &= Q(person__user__last_name__icontains=lastName)
            if firstName:
                query &= Q(person__user__first_name__icontains=firstName)
            if email:
                query &= Q(person__user__email__icontains=email)
            if branch:
                query &= Q(branch__title=branch)
            # if grade:
            #     query &= Q(grades__definition__name=grade, grades__status='Onayland??')
            # if visa == 'VISA':
            #     query &= Q(visa__startDate__year=timezone.now().year, visa__status='Onayland??')

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
            #     coachs = coachs.exclude(visa__startDate__year=timezone.now().year, visa__status='Onayland??')
    return render(request, 'TVGFBF/Coach/coach_serach.html',
                  {'coachs': coachs, 'user_form': user_form, 'branch': searchClupForm, 'clubs': clubs,
                   'current_date': current_date, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name, })


@login_required
def return_add_coach(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user_form = HavaUserForm()
    person_form = PersonForm()
    communication_form = CommunicationForm()
    clubs = Club.objects.all().exclude(derbis__isnull=True)

    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    if request.method == 'POST':
        with transaction.atomic():
            user_form = HavaUserForm(request.POST)
            person_form = PersonForm(request.POST, request.FILES)
            communication_form = CommunicationForm(request.POST)
            mail = request.POST.get('email')

            # if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
            #         email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
            #     email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
            #     email=mail):
            #     messages.warning(request, 'Mail adresi ba??ka bir kullanici taraf??ndan kullanilmaktadir.')
            #     return render(request, 'TVGFBF/Coach/add-coach.html',
            #                   {'user_form': user_form, 'person_form': person_form,
            #                    'communication_form': communication_form, 'urls': urls, 'current_url': current_url,
            #                    'url_name': url_name, 'clubs': clubs})

            tc = request.POST.get('tc')
            # if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
            #         tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
            #     tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
            #     messages.warning(request, 'Tc kimlik numarasi sisteme kay??tl??d??r. ')
            #     return render(request, 'TVGFBF/Coach/add-coach.html',
            #                   {'user_form': user_form, 'person_form': person_form,
            #                    'communication_form': communication_form, 'urls': urls, 'current_url': current_url,
            #                    'url_name': url_name, 'clubs': clubs})

            name = request.POST.get('first_name')
            surname = request.POST.get('last_name')
            year = request.POST.get('birthDate')
            year = year.split('/')

            # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
            # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
            #     messages.warning(request, 'Tc kimlik numarasi ile isim  soyisim dogum y??l??  bilgileri uyu??mamaktad??r. ')
            #     return render(request, 'TVGFBF/Coach/add-coach.html',
            #                   {'user_form': user_form, 'person_form': person_form,
            #                    'communication_form': communication_form, 'urls': urls, 'current_url': current_url,
            #                    'url_name': url_name, 'clubs': clubs})

            if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid():
                user = User()
                user.username = user_form.cleaned_data['email']
                user.first_name = user_form.cleaned_data['first_name']
                user.last_name = user_form.cleaned_data['last_name']
                user.email = user_form.cleaned_data['email']
                group = Group.objects.get(name='Antren??r')
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
                workplace = request.POST.get("workplace")
                person.workplace = workplace
                person.user = user
                communication = communication_form.save(commit=False)
                person.save()
                communication.save()

                coach = Coach(person=person, communication=communication)
                coach.save()

                clubDersbis = request.POST.get('club', None)
                if clubDersbis != 'noClub':
                    coachClub = Club.objects.get(derbis=clubDersbis)
                    coachClub.coachs.add(coach)
                    coachClub.save()
                # antroner kayd??ndan sonra mail g??nderilmeyecek

                # subject, from_email, to = 'Halter - Antren??r Bilgi Sistemi Kullan??c?? Giri?? Bilgileri', 'no-reply@twf.gov.tr', user.email
                # text_content = 'A??a????da ki bilgileri kullanarak sisteme giri?? yapabilirsiniz.'
                # html_content = '<p> <strong>Site adresi: </strong> <a href="http://sbs.twf.gov.tr:81/"></a>sbs.twf.gov.tr:81</p>'
                # html_content = html_content + '<p><strong>Kullan??c?? Ad??:  </strong>' + user.username + '</p>'
                # html_content = html_content + '<p><strong>??ifre: </strong>' + password + '</p>'
                # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()

                fdk = Forgot(user=user, status=False)
                fdk.save()

                # html_content = ''
                # subject, from_email, to = 'Bilgi Sistemi Kullan??c?? Bilgileri', 'no-reply@halter.gov.tr', user.email
                # html_content = '<h2>T??RK??YE HALTER FEDERASYONU B??LG?? S??STEM??</h2>'
                # html_content = html_content + '<p><strong>Kullan??c?? Ad??n??z :' + str(fdk.user.username) + '</strong></p>'
                # html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="https://sbs.halter.gov.tr:9443/newpassword?query=' + str(
                #     fdk.uuid) + '">https://sbs.halter.gov.tr:9443/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'
                # msg = EmailMultiAlternatives(subject, '', from_email, [to])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()

                messages.success(request, 'Antren??r Ba??ar??yla Kay??t Edilmi??tir.')

                return redirect('sbs:return_coachs')

            else:

                for x in user_form.errors.as_data():
                    messages.warning(request, user_form.errors[x][0])

    return render(request, 'TVGFBF/Coach/add-coach.html',
                  {'user_form': user_form, 'person_form': person_form,
                   'communication_form': communication_form, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name, 'clubs': clubs})


@login_required
def coachUpdate(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    coach = Coach.objects.get(uuid=uuid)
    coachclub = None
    if Club.objects.filter(coachs=coach):
        coachclub = Club.objects.filter(coachs=coach)
        clubs = Club.objects.exclude(coachs=coach).exclude(derbis__isnull=True)
    else:
        clubs = Club.objects.all().exclude(derbis__isnull=True)
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
        if mail != coach.user.email:

            if User.objects.filter(email=mail) or ReferenceCoach.objects.filter(
                    email=mail) or ReferenceReferee.objects.filter(email=mail) or PreRegistration.objects.filter(
                    email=mail):
                messages.warning(request, 'Mail adresi ba??ka bir kullanici taraf??ndan kullanilmaktadir.')
                return render(request, 'TVGFBF/Coach/update-coach.html',
                              {'user_form': user_form, 'communication_form': communication_form,
                               'person_form': person_form, 'grades_form': grade_form, 'coach': coach,
                               'personCoach': person, 'visa_form': visa_form, 'urls': urls, 'current_url': current_url,
                               'url_name': url_name, 'clubs': clubs, 'coachclub': coachclub})

        tc = request.POST.get('tc')
        if tc != coach.person.tc:
            if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                    tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
                tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
                messages.warning(request, 'Tc kimlik numarasi sisteme kay??tl??d??r. ')
                return render(request, 'TVGFBF/Coach/update-coach.html',
                              {'user_form': user_form, 'communication_form': communication_form,
                               'person_form': person_form, 'grades_form': grade_form, 'coach': coach,
                               'personCoach': person, 'visa_form': visa_form, 'urls': urls, 'current_url': current_url,
                               'url_name': url_name, 'clubs': clubs, 'coachclub': coachclub})

        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        year = request.POST.get('birthDate')
        year = year.split('/')

        client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
        if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
            messages.warning(request, 'Tc kimlik numarasi ile isim  soyisim dogum y??l??  bilgileri uyu??mamaktad??r. ')
            return render(request, 'TVGFBF/Coach/update-coach.html',
                          {'user_form': user_form, 'communication_form': communication_form,
                           'person_form': person_form, 'grades_form': grade_form, 'coach': coach,
                           'personCoach': person, 'visa_form': visa_form, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'clubs': clubs, 'coachclub': coachclub})

        if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid():

            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            user.save()

            user = user_form.save(commit=False)
            user.username = user_form.cleaned_data['email']
            user.save()

            log = str(user.get_full_name()) + " Antrenor g??ncelledi"
            log = general_methods.logwrite(request, request.user, log)

            person = person_form.save(commit=False)
            iban = request.POST.get("iban")
            if request.FILES.get('sgkUpdate'):
                coach.sgk = request.FILES.get('sgkUpdate')
            if request.FILES.get('coachFileUpdate'):
                coach.form = request.FILES.get('coachFileUpdate')
            clubDersbis = request.POST.get('club', None)
            if not clubDersbis == 'noRegister':
                coachClub = Club.objects.get(derbis=clubDersbis)
                coachClub.coachs.add(coach)
            else:
                if Club.objects.filter(coachs=coach):
                    club_coach = Club.objects.filter(coachs=coach).last()
                    club_coach.coachs.remove(coach)

            person.iban = iban
            person.save()
            coach.save()
            communication_form.save()

            messages.success(request, 'Antren??r Ba??ar??yla G??ncellendi')
            return redirect('sbs:return_coachs')
        else:
            messages.warning(request, 'Alanlar?? Kontrol Ediniz')

    return render(request, 'TVGFBF/Coach/update-coach.html',
                  {'user_form': user_form, 'communication_form': communication_form,
                   'person_form': person_form, 'grades_form': grade_form, 'coach': coach,
                   'personCoach': person, 'visa_form': visa_form, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name, 'clubs': clubs, 'coachclub': coachclub})


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

                if ReferenceCoach.objects.filter(email=obj.person.user.email):
                    coach = ReferenceCoach.objects.get(email=obj.person.user.email)
                    coach.status = coach.WAITED
                    coach.save()

                obj.delete()

                log = "Antren??r Sil"
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
        grade_form = GradeFormCoach(request.POST, request.FILES or None)

        if grade_form.is_valid() and request.POST.get(
                'branch') is not None:
            grade = HavaLevel(definition=grade_form.cleaned_data['definition'],
                              branch=grade_form.cleaned_data['branch'],
                              antrenorBelgesi=grade_form.cleaned_data['antrenorBelgesi'])
            grade.levelType = EnumFields.LEVELTYPE.GRADE
            grade.status = HavaLevel.WAITED
            grade.save()

            coach.grades.add(grade)
            coach.save()

            log = str(coach.person.user.get_full_name()) + " Kademe eklendi"
            log = general_methods.logwrite(request, request.user, log)

            messages.success(request, 'Kademe Ba??ar??yla Eklenmi??tir.')
            if request.user.groups.filter(name='Antren??r'):
                return redirect('sbs:updateProfileCoach')
            return redirect('sbs:update_coach', uuid=uuid)

        else:
            messages.warning(request, 'Alanlar?? Kontrol Ediniz')

    return render(request, 'TVGFBF/Coach/add-grade-coach.html',
                  {'grade_form': grade_form, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name, })


@login_required
def grade_approval(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                grade_uuid = request.POST['grade_uuid']
                coach_uuid = request.POST['coach_uuid']
                grade = HavaLevel.objects.get(uuid=grade_uuid)
                coach = Coach.objects.get(uuid=coach_uuid)
                for item in coach.grades.all():
                    if item.branch == grade.branch:
                        item.isActive = False
                        item.save()
                grade.status = HavaLevel.APPROVED
                grade.isActive = True
                date = request.POST['dateOfApproval']
                approvalDate = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                grade.approval_date = approvalDate
                grade.reject_text = ''
                grade.save()

                log = str(coach.person.user.get_full_name()) + " Kademe onaylandi"
                log = general_methods.logwrite(request, request.user, log)

                return JsonResponse({'status': 'Success', 'messages': 'Kademe Onaylanm????t??r.'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def grade_reject(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            grade = HavaLevel.objects.get(uuid=request.POST['grade_uuid'])
            grade.status = grade.DENIED
            date = request.POST['dateOfReject']
            text = request.POST['textOfReject']

            statusDate = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            grade.approval_date = statusDate
            grade.reject_text = text
            grade.save()

            coach = Coach.objects.get(uuid=request.POST['coach_uuid'])
            log = str(coach.person.user.get_full_name()) + " Kademe reddedildi"
            log = general_methods.logwrite(request, request.user, log)

            return JsonResponse({'status': 'Success', 'messages': 'Kademe Ba??ar??yla Reddedilmi??tir'})
        except HavaLevel.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


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
            messages.success(request, 'Kademe Ba??ar??l?? bir ??ekilde g??ncellenmi??tir.')
            return redirect('sbs:update_coach', uuid=coach_uuid)

        else:

            messages.warning(request, 'Alanlar?? Kontrol Ediniz')

    return render(request, 'TVGFBF/Coach/update-grade-coach.html',
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
                log = "Antren??r Kademe Sil"
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

                visa.definition = CategoryItem.objects.get(forWhichClazz='VISA_COACH')
                visa.levelType = EnumFields.LEVELTYPE.VISA
                visa.status = HavaLevel.WAITED

                visa.save()
                coach.visa.add(visa)
                coach.save()

                log = str(coach.person.user.get_full_name()) + " Antren??r  vize eklendi"
                log = general_methods.logwrite(request, request.user, log)

                messages.success(request, 'Vize Ba??ar??yla Eklenmi??tir.')
                if request.user.groups.filter(name='Antren??r'):
                    return redirect('sbs:updateProfileCoach')
                return redirect('sbs:update_coach', uuid=uuid)
        except:
            messages.warning(request, 'Alanlar?? Kontrol Ediniz')

    return render(request, 'TVGFBF/Coach/add-visa-coach.html',
                  {'visa_form': visa_form, 'category_item_form': category_item_form, 'urls': urls,
                   'current_url': current_url,
                   'url_name': url_name, })


@login_required
def visa_approval(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                visa_uuid = request.POST['visa_uuid']
                coach_uuid = request.POST['coach_uuid']
                visa = HavaLevel.objects.get(uuid=visa_uuid)
                visa.status = HavaLevel.APPROVED
                date = request.POST['dateOfApproval']
                approvalDate = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                visa.approval_date = approvalDate
                visa.reject_text = ''
                visa.save()
                visa.isActive = True
                coach = Coach.objects.filter(uuid=coach_uuid)
                if coach:
                    coach = Coach.objects.get(uuid=coach_uuid)

                    for item in coach.visa.all():
                        if item.branch == visa.branch:
                            item.isActive = False
                            item.save()
                    visa.isActive = True
                    visa.save()
                log = str(coach.person.user.get_full_name()) + " vize onaylandi"
                log = general_methods.logwrite(request, request.user, log)

                return JsonResponse({'status': 'Success', 'messages': 'Vize Onaylanm????t??r.'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


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

    messages.warning(request, 'Vize Reddedilmi??tir.')
    return redirect('sbs:update_coach', uuid=coach_uuid)


@login_required
def visa_update(request, visa_uuid, coach_uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    visa = HavaLevel.objects.get(uuid=visa_uuid)
    coach = Coach.objects.get(uuid=coach_uuid)
    visa_form = VisaForm(request.POST or None, request.FILES or None, instance=visa)

    if request.method == 'POST':
        if visa_form.is_valid():
            visa_form.save()
            if visa.status != HavaLevel.APPROVED:
                visa.status = HavaLevel.WAITED
                visa.save()

                log = str(coach.person.user.get_full_name()) + " antren??r  vize g??ncellendi"
                log = general_methods.logwrite(request, request.user, log)

                messages.success(request, 'Vize Ba??ar??yla G??ncellenmi??tir.')
                return redirect('sbs:update_coach', uuid=coach_uuid)
        else:
            messages.warning(request, 'Alanlar?? Kontrol Ediniz')

    return render(request, 'TVGFBF/Coach/update-visa-coach.html',
                  {'visa_form': visa_form, 'urls': urls,
                   'current_url': current_url,
                   'url_name': url_name})


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
                log = "Antren??r Vize Sil"
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
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    category_item_form = CategoryItemForm()

    if request.method == 'POST':

        category_item_form = CategoryItemForm(request.POST)

        if category_item_form.is_valid():

            categoryItem = CategoryItem(name=category_item_form.cleaned_data['name'])
            categoryItem.forWhichClazz = "COACH_GRADE"
            categoryItem.save()

            return redirect('sbs:return_grade')

        else:

            messages.warning(request, 'Alanlar?? Kontrol Ediniz')
    categoryitem = CategoryItem.objects.filter(forWhichClazz="COACH_GRADE", isDeleted=0).order_by('order')
    return render(request, 'TVGFBF/Coach/grades.html',
                  {'category_item_form': category_item_form, 'categoryitem': categoryitem, 'urls': urls,
                   'current_url': current_url,
                   'url_name': url_name})


@login_required
def gradeUpdate(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    categoryItem = CategoryItem.objects.get(uuid=uuid)
    category_item_form = CategoryItemForm(request.POST or None, instance=categoryItem)
    if request.method == 'POST':
        if category_item_form.is_valid():
            category = category_item_form.save(request, commit=False)
            category.save()
            messages.success(request, 'Ba??ar??yla G??ncellendi')
            return redirect('sbs:return_grade')
        else:
            messages.warning(request, 'Alanlar?? Kontrol Ediniz')

    return render(request, 'TVGFBF/Coach/update-grade.html',
                  {'category_item_form': category_item_form, 'urls': urls,
                   'current_url': current_url,
                   'url_name': url_name})


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
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    coa = []
    for item in CategoryItem.objects.filter(forWhichClazz='COACH_GRADE'):
        coa.append(item.pk)
    grade = HavaLevel.objects.filter(definition_id__in=coa, levelType=EnumFields.LEVELTYPE.GRADE,
                                     isDeleted=0).distinct()

    return render(request, 'TVGFBF/Coach/coach-grade-list.html',
                  {'coachGrades': grade, 'urls': urls,
                   'current_url': current_url,
                   'url_name': url_name})


@login_required
def gradeListApproval(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                grade_uuid = request.POST['grade_uuid']
                grade = HavaLevel.objects.get(uuid=grade_uuid)
                date = request.POST['dateOfApproval']
                approvalDate = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                grade.approval_date = approvalDate
                if grade.CoachGrades.first():
                    coach = grade.CoachGrades.first()
                    for item in coach.grades.all():
                        if item.branch == grade.branch:
                            item.isActive = False
                            item.save()
                grade.status = HavaLevel.APPROVED
                grade.isActive = True
                grade.reject_text = ''
                grade.save()

                return JsonResponse({'status': 'Success', 'messages': 'Kademe Onaylanm????t??r.'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def gradeListReject(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            grade = HavaLevel.objects.get(uuid=request.POST['uuid'])
            grade.status = grade.DENIED
            date = request.POST['dateOfReject']
            text = request.POST['textOfReject']

            statusDate = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            grade.approval_date = statusDate
            grade.reject_text = text
            grade.save()

            log = str(grade.definition.name) + "     Antren??r kademe basvurusu reddedildi"
            log = general_methods.logwrite(request, request.user, log)

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except HavaLevel.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def gradeListApprovalAll(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    coa = []
    try:
        if request.method == 'POST' and request.is_ajax():
            for item in CategoryItem.objects.filter(forWhichClazz='COACH_GRADE'):
                coa.append(item.pk)
            grades = HavaLevel.objects.filter(definition_id__in=coa, levelType=EnumFields.LEVELTYPE.GRADE,
                                              status="Beklemede")

            for grade in grades:
                coach = grade.CoachGrades.first()

                for item in coach.grades.all():
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
    coa = []
    try:
        if request.method == 'POST' and request.is_ajax():
            for item in CategoryItem.objects.filter(forWhichClazz='COACH_GRADE'):
                coa.append(item.pk)
            grades = HavaLevel.objects.filter(definition_id__in=coa, levelType=EnumFields.LEVELTYPE.GRADE,
                                              status="Beklemede")
            for grade in grades:
                grade.status = HavaLevel.DENIED
                grade.save()
            messages.success(request, 'Beklemede olan kademeler   Reddedilmi??tir.')
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
    for item in CategoryItem.objects.filter(forWhichClazz='VISA_COACH'):
        coa.append(item.pk)
    visa = HavaLevel.objects.filter(definition_id__in=coa, levelType=EnumFields.VISA, isDeleted=0).distinct()
    return render(request, 'TVGFBF/Coach/coach-visa-list.html',
                  {'coachvisas': visa, 'urls': urls,
                   'current_url': current_url,
                   'url_name': url_name})


@login_required
def visaListApproval(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                visa_uuid = request.POST['visa_uuid']
                visa = HavaLevel.objects.get(uuid=visa_uuid)
                date = request.POST['dateOfApproval']
                approvalDate = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                visa.approval_date = approvalDate
                visa.status = HavaLevel.APPROVED
                if visa.CoachVisa.first():
                    coach = visa.CoachVisa.first()
                    for item in coach.visa.all():
                        if item.branch == visa.branch:
                            item.isActive = False
                            item.save()
                visa.isActive = True
                visa.reject_text = ''
                visa.save()
                return JsonResponse({'status': 'Success', 'messages': 'Vize Onaylanm????t??r.'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def visaListReject(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            visa = HavaLevel.objects.get(uuid=request.POST['uuid'])
            visa.status = HavaLevel.DENIED
            date = request.POST['dateOfReject']
            text = request.POST['textOfReject']

            statusDate = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            visa.approval_date = statusDate
            visa.reject_text = text
            visa.save()

            log = str(visa.definition.name) + "     Antren??r vize basvurusu reddedildi"
            log = general_methods.logwrite(request, request.user, log)

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except HavaLevel.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def returnVisaSeminarApplication(request):
    perm = general_methods.control_access_klup(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    basvurularim = CoachApplication.objects.none()
    coach = Coach.objects.get(person__user=user)
    if request.user.groups.filter(name='Antren??r').exists():
        seminar = VisaSeminar.objects.filter(coachApplication__coach__user=user).filter(
            forWhichClazz='COACH').distinct()
        basvurularim = CoachApplication.objects.filter(coach__user=user)

    else:
        seminar = VisaSeminar.objects.filter(forWhichClazz='COACH')

    return render(request, 'TVGFBF/Coach/visa-seminar.html',
                  {'seminer': seminar, 'basvuru': basvurularim, 'coach': coach})


@login_required
def returnVisaSeminar(request):
    perm = general_methods.control_access_klup(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    user = request.user
    seminar = VisaSeminar.objects.filter(forWhichClazz='COACH', isDeleted=0)

    if request.method == 'POST':
        if user.groups.filter(name='Antren??r').exists():
            vizeSeminer = VisaSeminar.objects.get(pk=request.POST.get('pk'))
            coach = Coach.objects.get(person__user=request.user)
            try:
                if request.FILES['file']:
                    document = request.FILES['file']
                    data = CoachApplication()
                    data.dekont = document
                    data.coach = coach
                    data.save()
                    vizeSeminer.coachApplication.add(data)
                    vizeSeminer.save()

                    messages.success(request, 'Vize Seminerine Ba??vuru  ger??ekle??mi??tir.')
                    return redirect('sbs:return-coach-visa-seminar-application')


            except:
                messages.warning(request, 'L??tfen yeniden deneyiniz')

    return render(request, 'TVGFBF/Coach/coach-visa-seminar.html', {'competitions': seminar, 'urls': urls,
                                                                    'current_url': current_url,
                                                                    'url_name': url_name})


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
    if request.method == 'POST':
        visaSeminar = VisaSeminarForm(request.POST)
        if visaSeminar.is_valid():

            visa = visaSeminar.save()
            visa.forWhichClazz = 'COACH'
            visa.save()
            messages.success(request, 'Vize Semineri Ba??ari  Kaydedilmi??tir.')

            return redirect('sbs:coach-visa-seminar')
        else:

            messages.warning(request, 'Alanlar?? Kontrol Ediniz')

    return render(request, 'TVGFBF/Coach/add-visa-seminar-coach.html',
                  {'competition_form': visaSeminar, 'urls': urls,
                   'current_url': current_url,
                   'url_name': url_name})


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
            messages.success(request, 'Vize Seminer Ba??ar??yla G??ncellenmi??tir.')

            return redirect('sbs:coach-visa-seminar')
        else:

            messages.warning(request, 'Alanlar?? Kontrol Ediniz')

    return render(request, 'TVGFBF/Coach/update-coach-visa-seminar.html',
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
                obj.delete()

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except VisaSeminar.DoesNotExist:
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
        messages.warning(request, 'Seminer Daha ??nce Onaylanmistir.')

    return redirect('sbs:update-coach-visa-seminar', uuid=uuid)


@login_required
def addCoachVisaSeminar(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    visa = VisaSeminar.objects.get(uuid=uuid)

    return render(request, 'TVGFBF/Coach/add-coach-visa-seminar.html', {'uuid': uuid, })


@login_required
def addCaochVisaSeminarApi(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():

            if request.method == 'POST' and request.is_ajax():
                list = request.POST.getlist('coach_list[]')
                visa = VisaSeminar.objects.get(uuid=request.POST['uuid'])
                for item in list:
                    if not visa.coach.filter(person__user_id__in=item):
                        visa.coach.add(item)
                        visa.save()

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


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
                html_content = '<h2>T??RK??YE HALTER FEDERASYONU B??LG?? S??STEM??</h2>'
                html_content = '<p><strong>' + str(seminer.name) + '</strong> Seminer  ba??vurunuz reddedilmi??tir.</p>'

                msg = EmailMultiAlternatives(subject, '', from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                log = str(seminer.name) + "    seminer basvusu reddedilmi??tir    " + str(
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
                html_content = '<h2>T??RK??YE HALTER FEDERASYONU B??LG?? S??STEM??</h2>'
                html_content = '<p><strong>' + str(seminer.name) + '</strong> Seminer  ba??vurunuz onaylanm????t??r.</p>'

                msg = EmailMultiAlternatives(subject, '', from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                log = str(seminer.name) + "    seminer basvusu onaylanm????t??r    " + str(
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


@login_required
def detailCoach(request):
    # perm = general_methods.control_access(request)
    #
    # if not perm:
    #     logout(request)
    #     return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']

                obj = Coach.objects.get(uuid=uuid)
                coachs = {}
                coachs['name'] = obj.person.user.get_full_name()
                coachs['tc'] = obj.person.tc
                coachs['email'] = obj.person.user.email
                coachs['phone'] = obj.communication.phoneNumber
                coachs['image'] = obj.person.profileImage.url
                branchs = ''
                for branch in obj.branch.all():
                    branchs = branchs + branch.title + ','
                coachs['branch'] = branchs
                club = ''
                if Club.objects.filter(coachs=obj):
                    club = Club.objects.get(coachs=obj).name
                coachs['club'] = club
                grade_info = {}
                visa_info = {}
                finishDate = ''
                startDate = ''
                finishDate_visa = ''
                startDate_visa = ''
                visa_name = ''
                grade_name = ''
                if obj.grades.filter(isActive=True):
                    grade = obj.grades.filter(isActive=True).last()
                    if grade.expireDate:
                        finishDate = grade.expireDate
                    if grade.startDate:
                        startDate = grade.startDate
                    grade_name = grade.definition.name
                if obj.visa.filter(isActive=True):
                    visa = obj.visa.filter(isActive=True).last()
                    if visa.expireDate:
                        finishDate_visa = visa.expireDate
                    if visa.startDate:
                        startDate_visa = visa.startDate
                    visa_name = visa.definition.name
                grade_info['finishDate'] = finishDate
                grade_info['startDate'] = startDate
                grade_info['name'] = grade_name
                visa_info['name'] = visa_name
                visa_info['finishDate'] = finishDate_visa
                visa_info['startDate'] = startDate_visa
                coachs['grade'] = grade_info
                coachs['visa'] = visa_info

                return JsonResponse({'status': 'Success',
                                     'results': coachs,
                                     })
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except Coach.DoesNotExist:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def antrenor(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    status = ReferenceCoach.STATUS_CHOICES
    return render(request, 'TVGFBF/Coach/reference-list-coach.html', {'urls': urls,
                                                                      'current_url': current_url,
                                                                      'url_name': url_name, 'status': status})


@login_required
def coachreferenceUpdate(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    currentCoach = ReferenceCoach.objects.get(uuid=uuid)
    countries = Country.objects.exclude(id=currentCoach.country.pk).order_by('order')
    currentCountry = currentCoach.country
    cities = City.objects.all().exclude(id=currentCoach.city.pk)
    currentCity = currentCoach.city
    if currentCoach.kademe_definition:
        grades = CategoryItem.objects.filter(forWhichClazz="COACH_GRADE", isDeleted=0).exclude(
            id=currentCoach.kademe_definition.pk).order_by('order')
    else:
        grades = CategoryItem.objects.filter(forWhichClazz="COACH_GRADE", isDeleted=0).order_by('order')
    if currentCoach.kademe_definition2:
        grades2 = CategoryItem.objects.filter(forWhichClazz="COACH_GRADE", isDeleted=0).exclude(
            id=currentCoach.kademe_definition2.pk).order_by('order')
    else:
        grades2 = CategoryItem.objects.filter(forWhichClazz="COACH_GRADE", isDeleted=0).order_by('order')
    if currentCoach.kademe_brans:
        branchs = Branch.objects.filter(isDeleted=0).exclude(uuid=currentCoach.kademe_brans.uuid)
    else:
        branchs = Branch.objects.filter(isDeleted=0)
    if currentCoach.kademe_brans2:
        branchs2 = Branch.objects.filter(isDeleted=0).exclude(uuid=currentCoach.kademe_brans2.uuid)
    else:
        branchs2 = Branch.objects.filter(isDeleted=0)
    if currentCoach.vize_brans:
        visaBranchs = Branch.objects.filter(isDeleted=0).exclude(uuid=currentCoach.vize_brans.uuid)
    else:
        visaBranchs = Branch.objects.filter(isDeleted=0)
    if currentCoach.vize_brans2:
        visaBranchs2 = Branch.objects.filter(isDeleted=0).exclude(uuid=currentCoach.vize_brans2.uuid)
    else:
        visaBranchs2 = Branch.objects.filter(isDeleted=0)
    if currentCoach.club:
        clubs = Club.objects.all().exclude(derbis__isnull=True).exclude(id=currentCoach.club.pk)
        currentClub = currentCoach.club
    else:
        clubs = Club.objects.all().exclude(derbis__isnull=True)
        currentClub = None
    try:
        with transaction.atomic():
            if request.method == 'POST':
                # coach = ReferenceCoach.objects.get(uuid=uuid)
                mail = request.POST.get('emailUpdate')
                if ReferenceCoach.objects.exclude(uuid=currentCoach.uuid).filter(email=mail) or User.objects.filter(
                        email=mail) or ReferenceReferee.objects.filter(email=mail) or PreRegistration.objects.filter(
                    email=mail):
                    messages.warning(request, 'Mail adresi  sistemde  kay??tl??d??r. ')
                    return render(request, 'TVGFBF/Coach/referenceCoachUpdate.html',
                                  {'currentCoach': currentCoach, 'clubs': clubs, 'currentClub': currentClub,
                                   'urls': urls,
                                   'current_url': current_url, 'url_name': url_name, 'countries': countries,
                                   'currentCountry': currentCountry, 'cities': cities, 'currentCity': currentCity,
                                   'grades': grades, 'branchs': branchs, 'visaBranchs': visaBranchs, 'grades2': grades2,
                                   'branchs2': branchs2, 'visaBranchs2': visaBranchs2})

                tc = request.POST.get('tcUpdate')
                if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(uuid=currentCoach.uuid).filter(
                        tc=tc) or ReferenceReferee.objects.filter(tc=tc) or PreRegistration.objects.filter(tc=tc):
                    messages.warning(request, 'Tc kimlik numarasi sistemde  kay??tl??d??r. ')
                    return render(request, 'TVGFBF/Coach/referenceCoachUpdate.html',
                                  {'currentCoach': currentCoach, 'clubs': clubs, 'currentClub': currentClub,
                                   'urls': urls,
                                   'current_url': current_url, 'url_name': url_name, 'countries': countries,
                                   'currentCountry': currentCountry, 'cities': cities, 'currentCity': currentCity,
                                   'grades': grades, 'branchs': branchs, 'visaBranchs': visaBranchs, 'grades2': grades2,
                                   'branchs2': branchs2, 'visaBranchs2': visaBranchs2})

                name = request.POST.get('firstNameUpdate')
                surname = request.POST.get('lastNameUpdate')
                year = request.POST.get('birthDateUpdate')
                year = year.split('/')

                client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
                if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
                    messages.warning(request,
                                     'Tc kimlik numarasi ile isim  soyisim dogum y??l??  bilgileri uyu??mamaktad??r. ')
                    return render(request, 'TVGFBF/Coach/referenceCoachUpdate.html',
                                  {'currentCoach': currentCoach, 'clubs': clubs, 'currentClub': currentClub,
                                   'urls': urls,
                                   'current_url': current_url, 'url_name': url_name, 'countries': countries,
                                   'currentCountry': currentCountry, 'cities': cities, 'currentCity': currentCity,
                                   'grades': grades, 'branchs': branchs, 'visaBranchs': visaBranchs, 'grades2': grades2,
                                   'branchs2': branchs2, 'visaBranchs2': visaBranchs2})

                if request.FILES.get('profileImageUpdate'):
                    currentCoach.profileImage = request.FILES.get('profileImageUpdate')
                currentCoach.first_name = request.POST.get('firstNameUpdate')
                currentCoach.last_name = request.POST.get('lastNameUpdate')
                currentCoach.birthplace = request.POST.get('birthPlaceUpdate')
                currentCoach.iban = request.POST.get('ibanUpdate')
                currentCoach.workplace = request.POST.get('workplaceUpdate')
                currentCoach.tc = request.POST.get('tcUpdate')
                currentCoach.motherName = request.POST.get('motherNameUpdate')
                currentCoach.fatherName = request.POST.get('fatherNameUpdate')
                currentCoach.postalCode = request.POST.get('postalCodeUpdate')
                birthDate = request.POST.get('birthDateUpdate')
                currentCoach.birthDate = datetime.datetime.strptime(birthDate, "%d/%m/%Y").strftime("%Y-%m-%d")
                currentCoach.gender = request.POST.get('genderUpdate', None)
                if Club.objects.filter(derbis=request.POST.get('clubUpdate')):
                    currentCoach.club = Club.objects.get(derbis=request.POST.get('clubUpdate'))
                elif request.POST.get('clubUpdate') == '':
                    currentCoach.club = None
                currentCoach.email = request.POST.get('emailUpdate')
                currentCoach.phoneNumber = request.POST.get('phoneNumberUpdate')
                currentCoach.phoneNumber2 = request.POST.get('phoneNumber2Update')
                if Country.objects.filter(uuid=request.POST.get('countryUpdate')):
                    currentCoach.country = Country.objects.get(uuid=request.POST.get('countryUpdate'))
                if City.objects.filter(uuid=request.POST.get('cityUpdate')):
                    currentCoach.city = City.objects.get(uuid=request.POST.get('cityUpdate'))
                currentCoach.address = request.POST.get('addressUpdate')

                if request.POST.get('gradeUpdateVucut'):
                    currentCoach.kademe_definition = CategoryItem.objects.get(uuid=request.POST.get('gradeUpdateVucut'))
                if request.POST.get('branchUpdateVucut'):
                    currentCoach.kademe_brans = Branch.objects.get(uuid=request.POST.get('branchUpdateVucut'))
                if request.FILES.get('belgeUpdateVucut'):
                    currentCoach.belge = request.FILES.get('belgeUpdateVucut')

                if request.POST.get('gradeUpdateBilek'):
                    currentCoach.kademe_definition2 = CategoryItem.objects.get(
                        uuid=request.POST.get('gradeUpdateBilek'))
                if request.POST.get('branchUpdateBilek'):
                    currentCoach.kademe_brans2 = Branch.objects.get(uuid=request.POST.get('branchUpdateBilek'))
                if request.FILES.get('belgeUpdateBilek'):
                    currentCoach.belge2 = request.FILES.get('belgeUpdateBilek')

                if request.POST.get('visaBranchUpdateVucut'):
                    currentCoach.vize_brans = Branch.objects.get(uuid=request.POST.get('visaBranchUpdateVucut'))
                if request.FILES.get('dekontUpdateVucut'):
                    currentCoach.dekont = request.FILES.get('dekontUpdateVucut')

                if request.POST.get('visaBranchUpdateBilek'):
                    currentCoach.vize_brans2 = Branch.objects.get(uuid=request.POST.get('visaBranchUpdateBilek'))
                if request.FILES.get('dekontUpdateBilek'):
                    currentCoach.dekont2 = request.FILES.get('dekontUpdateBilek')

                # if request.POST.get('checkDekont'):
                #     currentCoach.dekont = None
                # elif request.FILES.get('dekontUpdate'):
                #     currentCoach.dekont = request.FILES.get('dekontUpdate')

                if request.FILES.get('kademeBelgeUpdate'):
                    currentCoach.kademe_belge = request.FILES.get('kademeBelgeUpdate')
                if request.FILES.get('sgkUpdate'):
                    currentCoach.sgk = request.FILES.get('sgkUpdate')
                currentCoach.save()

                messages.success(request, 'Antren??r Ba??vurusu G??ncellendi')
                return redirect("sbs:coach-application")

            return render(request, 'TVGFBF/Coach/referenceCoachUpdate.html',
                          {'currentCoach': currentCoach, 'clubs': clubs, 'currentClub': currentClub, 'urls': urls,
                           'current_url': current_url, 'url_name': url_name, 'countries': countries,
                           'currentCountry': currentCountry, 'cities': cities, 'currentCity': currentCity,
                           'grades': grades, 'branchs': branchs, 'visaBranchs': visaBranchs, 'grades2': grades2,
                           'branchs2': branchs2, 'visaBranchs2': visaBranchs2})
    except Exception as e:
        messages.warning(request, 'HATA !! ' + ' ' + str(e))
        return render(request, 'TVGFBF/Coach/referenceCoachUpdate.html',
                      {'currentCoach': currentCoach, 'clubs': clubs, 'currentClub': currentClub, 'urls': urls,
                       'current_url': current_url, 'url_name': url_name, 'countries': countries,
                       'currentCountry': currentCountry, 'cities': cities, 'currentCity': currentCity,
                       'grades': grades, 'branchs': branchs, 'visaBranchs': visaBranchs, 'grades2': grades2,
                       'branchs2': branchs2, 'visaBranchs2': visaBranchs2})


@login_required
def approvelReferenceCoach(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                referenceCoach = ReferenceCoach.objects.get(uuid=uuid)
                date = request.POST['dateOfApproval']
                approvalDate = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                referenceCoach.status_date = approvalDate

                if referenceCoach.status == ReferenceCoach.WAITED or referenceCoach.status == ReferenceCoach.DENIED:
                    if referenceCoach.kademe_definition and referenceCoach.belge and referenceCoach.kademe_brans:
                        grade = HavaLevel(definition=referenceCoach.kademe_definition,
                                          antrenorBelgesi=referenceCoach.belge,
                                          branch=referenceCoach.kademe_brans)
                        grade.levelType = EnumFields.LEVELTYPE.GRADE
                        grade.status = HavaLevel.APPROVED
                        grade.isActive = True
                        grade.approval_date = approvalDate
                        grade.save()
                    else:
                        if referenceCoach.kademe_definition or referenceCoach.belge or referenceCoach.kademe_brans:
                            messages.warning(request, 'Kademe bilgisi eklenemedi. Eksik kademe bilgilerini doldurunuz.')
                            return JsonResponse(
                                {'status': 'Fail',
                                 'msg': 'Kademe bilgisi eksik oldu??u i??in kay??t onaylanamad??. Eksik kademe bilgilerini doldurunuz.'})

                    if referenceCoach.kademe_definition2 and referenceCoach.belge2 and referenceCoach.kademe_brans2:
                        grade2 = HavaLevel(definition=referenceCoach.kademe_definition2,
                                           antrenorBelgesi=referenceCoach.belge2,
                                           branch=referenceCoach.kademe_brans2)
                        grade2.levelType = EnumFields.LEVELTYPE.GRADE
                        grade2.status = HavaLevel.APPROVED
                        grade2.isActive = True
                        grade2.approval_date = approvalDate
                        grade2.save()
                    else:
                        if referenceCoach.kademe_definition2 or referenceCoach.belge2 or referenceCoach.kademe_brans2:
                            messages.warning(request, 'Kademe bilgisi eklenemedi. Eksik kademe bilgilerini doldurunuz.')
                            return JsonResponse(
                                {'status': 'Fail',
                                 'msg': '2. Kademe bilgisi eksik oldu??u i??in kay??t onaylanamad??. Eksik kademe bilgilerini doldurunuz.'})

                    if referenceCoach.vize_brans and referenceCoach.dekont:
                        visa = HavaLevel(dekont=referenceCoach.dekont, branch=referenceCoach.vize_brans)
                        visa.levelType = EnumFields.LEVELTYPE.VISA
                        visa.status = HavaLevel.APPROVED
                        visa.isActive = True
                        visa.approval_date = approvalDate
                        visa.save()
                    else:
                        if referenceCoach.vize_brans or referenceCoach.dekont:
                            messages.warning(request, 'Vize bilgisi eklenemedi. Eksik vize bilgilerini doldurunuz.')
                            return JsonResponse(
                                {'status': 'Fail',
                                 'msg': 'Vize bilgisi eksik oldu??u i??in kay??t onaylanamad??. Eksik vize bilgilerini doldurunuz.'})

                    if referenceCoach.vize_brans2 and referenceCoach.dekont2:
                        visa2 = HavaLevel(dekont=referenceCoach.dekont2, branch=referenceCoach.vize_brans2)
                        visa2.levelType = EnumFields.LEVELTYPE.VISA
                        visa2.status = HavaLevel.APPROVED
                        visa2.isActive = True
                        visa2.approval_date = approvalDate
                        visa2.save()
                    else:
                        if referenceCoach.vize_brans2 or referenceCoach.dekont2:
                            messages.warning(request, 'Vize bilgisi eklenemedi. Eksik vize bilgilerini doldurunuz.')
                            return JsonResponse(
                                {'status': 'Fail',
                                 'msg': '2.Vize bilgisi eksik oldu??u i??in kay??t onaylanamad??. Eksik vize bilgilerini doldurunuz.'})
                    user = User()
                    user.username = referenceCoach.email
                    user.first_name = referenceCoach.first_name
                    user.last_name = referenceCoach.last_name
                    user.email = referenceCoach.email
                    password = User.objects.make_random_password()
                    user.set_password(password)
                    user.is_active = True
                    group = Group.objects.get(name='Antren??r')

                    user.save()

                    user.groups.add(group)

                    user.save()

                    person = Person()
                    person.tc = referenceCoach.tc
                    person.motherName = referenceCoach.motherName
                    person.fatherName = referenceCoach.fatherName
                    person.profileImage = referenceCoach.profileImage
                    person.birthDate = referenceCoach.birthDate
                    person.birthplace = referenceCoach.birthplace
                    person.bloodType = referenceCoach.bloodType
                    person.iban = referenceCoach.iban
                    if referenceCoach.gender == 'Erkek':
                        person.gender = Person.MALE
                    else:
                        person.gender = Person.FEMALE
                    person.save()
                    person.user = user
                    person.save()

                    communication = Communication()
                    communication.postalCode = referenceCoach.postalCode
                    communication.phoneNumber = referenceCoach.phoneNumber
                    communication.phoneNumber2 = referenceCoach.phoneNumber2
                    communication.address = referenceCoach.address
                    communication.city = referenceCoach.city
                    communication.country = referenceCoach.country
                    communication.save()

                    coach = Coach(person=person, communication=communication, sgk=referenceCoach.sgk,
                                  form=referenceCoach.kademe_belge)
                    coach.workplace = referenceCoach.workplace

                    coach.save()

                    if referenceCoach.kademe_definition and referenceCoach.belge and referenceCoach.kademe_brans:
                        coach.grades.add(grade)
                    if referenceCoach.kademe_definition2 and referenceCoach.belge2 and referenceCoach.kademe_brans2:
                        coach.grades.add(grade2)
                    if referenceCoach.vize_brans and referenceCoach.dekont:
                        coach.visa.add(visa)
                    if referenceCoach.vize_brans2 and referenceCoach.dekont2:
                        coach.visa.add(visa2)


                    messages.success(request, 'Antren??r Ba??ar??yla Eklenmi??tir')
                    referenceCoach.status = ReferenceCoach.APPROVED
                    referenceCoach.definition = ''
                    referenceCoach.save()

                    fdk = Forgot(user=user, status=False)
                    fdk.save()

                    if referenceCoach.club:
                        referenceCoach.club.coachs.add(coach)

                    html_content = ''
                    subject, from_email, to = 'Bilgi Sistemi Antren??r Kullan??c?? Bilgileri', EMAIL_HOST_USER, user.email
                    html_content = '<h2>T??RK??YE V??CUT GEL????T??RME F??TNESS VE B??LEK G??RE???? FEDERASYONU B??LG?? S??STEM??</h2>'
                    html_content = html_content + '<p>Ba??vurunuz Onaylanm????t??r.</p>'
                    html_content = html_content + '<p><strong>Kullan??c?? Ad??n??z :' + str(
                        user.username) + '</strong></p>'
                    html_content = html_content + '<p><strong>??ifreniz :' + str(password) + '</strong></p>'
                    html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="https://sbs.tvgfbf.gov.tr/">https://sbs.tvgfbf.gov.tr/</p></a>'
                    msg = EmailMultiAlternatives(subject, '', from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    log = str(user.get_full_name()) + " Antren??r ba??vurusu onaylandi"
                    log = general_methods.logwrite(request, request.user, log)

                    return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

                else:
                    referenceCoach.status = ReferenceCoach.APPROVED
                    referenceCoach.save()
                    messages.success(request, 'Antren??r daha ??nce onaylanm????t??r.')
                    return JsonResponse({'status': 'Success', 'msg': 'Antren??r daha ??nce onylanm????t??r.'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except referenceCoach.DoesNotExist:
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def refencedeleteCoach(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = ReferenceCoach.objects.get(uuid=request.POST['uuid'])
            obj.status = ReferenceCoach.DENIED
            date = request.POST['dateOfReject']
            text = request.POST['textOfReject']

            statusDate = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            obj.status_date = statusDate
            obj.definition = text
            obj.save()

            html_content = ''
            subject, from_email, to = 'Bilgi Sistemi Ba??vuru Sonucu', EMAIL_HOST_USER, obj.email
            html_content = '<h2>T??RK??YE V??CUT GEL????T??RME F??TNESS VE B??LEK G??RE???? FEDERASYONU B??LG?? S??STEM??</h2>'
            html_content = html_content + '<p>Ba??vurunuz Reddedilmi??tir.</p>'
            html_content = html_content + '<p style="color: red">Reddedilme Nedeni : ' + text + '</p>'
            html_content = html_content + '<h3 style="color: red">UYARI  !! Bilgilerinizi Do??ru ve G??ncel Girmedi??iniz Takdirde Yasal ????lem Ba??lat??lacakt??r.</h3>'

            msg = EmailMultiAlternatives(subject, '', from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            log = str(obj.first_name) + " " + str(obj.last_name) + "     Antren??r basvurusu reddedildi"
            log = general_methods.logwrite(request, request.user, log)

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Coach.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def registerCoachDelete(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = ReferenceCoach.objects.get(uuid=request.POST['uuid'])
            obj.delete()

            log = str(obj.first_name) + " " + str(obj.last_name) + "     Antren??r basvurusu silindi"
            log = general_methods.logwrite(request, request.user, log)

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Coach.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
