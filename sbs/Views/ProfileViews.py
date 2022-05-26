from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import redirect, render

from sbs.Forms.havaspor.CoachForm import CoachForm
from sbs.Forms.havaspor.GradeFormCoach import GradeFormCoach
from sbs.Forms.havaspor.HavaUserForm import HavaUserForm
from sbs.Forms.havaspor.PersonForm import PersonForm
from sbs.Forms.havaspor.ProfileCommunicationForm import ProfileCommunicationForm
from sbs.Forms.havaspor.RefereeForm import RefereeForm
from sbs.Forms.havaspor.VisaForm import VisaForm
from sbs.models import Coach, Person, Communication, Referee, SportClubUser
from sbs.services import general_methods


@login_required
def updateProfileCoach(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    user = request.user
    coach = Coach.objects.get(person__user=user)
    person = Person.objects.get(pk=coach.person.pk)
    communication = Communication.objects.get(pk=coach.communication.pk)
    user_form = HavaUserForm(request.POST or None, instance=user)
    person_form = PersonForm(request.POST or None, instance=person)
    communication_form = ProfileCommunicationForm(request.POST or None, instance=communication)
    coach_form = CoachForm(request.POST or None, request.FILES or None, instance=coach)
    password_form = SetPasswordForm(request.user, request.POST)
    iban = coach.person.iban
    grade_form = None
    visa_form = None
    if not coach.grades.all():
        grade_form = GradeFormCoach(request.POST or None, request.FILES or None, prefix='grade')
    else:

        grade = coach.grades.order_by('-expireDate').first()
        grade_form = GradeFormCoach(request.POST or None, request.FILES or None, prefix='grade', instance=grade)
        # if grade.form:
        #     grade_form.fields['form'].widget.attrs['readonly'] = 'readonly'
        # if grade.dekont:
        #     grade_form.fields['dekont'].widget.attrs['readonly'] = 'readonly'
        # if grade.startDate:
        #     grade_form.fields['startDate'].widget.attrs['readonly'] = 'readonly'
        #     grade_form.fields['startDate'].widget.attrs['required'] = False
        #
        # if grade.branch:
        #     grade_form.fields['branch'].widget.attrs['readonly'] = 'readonly'
        # if grade.definition:
        #     grade_form.fields['definition'].widget.attrs['readonly'] = 'readonly'

    if not coach.visa.all():
        visa_form = VisaForm(request.POST or None, request.FILES or None, prefix='visa')
    else:
        visa = coach.visa.order_by('-expireDate').first()
        visa_form = VisaForm(request.POST or None, request.FILES or None, prefix='visa', instance=visa)
        # if visa.form:
        #     visa_form.fields['form'].widget.attrs['readonly'] = 'readonly'
        # if visa.dekont:
        #     visa_form.fields['dekont'].widget.attrs['readonly'] = 'readonly'
        # if visa.startDate:
        #     visa_form.fields['startDate'].widget.attrs['readonly'] = 'readonly'
        #     visa_form.fields['startDate'].widget.attrs['required'] = False
        #
        # if visa.branch:
        #     visa_form.fields['branch'].widget.attrs['readonly'] = 'readonly'

    if request.method == 'POST':

        if request.POST['save_button'] == 'profile':
            if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid():
                user.username = user_form.cleaned_data['email']
                user.first_name = user_form.cleaned_data['first_name']
                user.last_name = user_form.cleaned_data['last_name']
                user.email = user_form.cleaned_data['email']
                user.save()
                person_form.save(request)
                iban = request.POST['iban']
                person.iban = iban
                person.save()
                communication_form.save(request)
                messages.success(request, 'Profil Bilgileri Başarıyla Güncellenmiştir.')

                return redirect('sbs:updateProfileCoach')
            else:

                messages.warning(request, 'Alanları Kontrol Ediniz')

        elif request.POST['save_button'] == 'password':
            if password_form.is_valid():

                user.set_password(password_form.cleaned_data['new_password1'])
                user.save()

                messages.success(request, 'Şifre Bilgileri Başarıyla Güncellenmiştir.')

                return redirect('sbs:updateProfileCoach')
            else:

                messages.warning(request, 'Alanları Kontrol Ediniz')


        else:
            if coach_form.is_valid():
                coach_form.save()

            else:

                messages.warning(request, 'Alanları Kontrol Ediniz')
                return redirect('sbs:updateProfileCoach')

            if grade_form.is_valid():
                grade = grade_form.save()
                if not coach.grades.all():
                    coach.grades.add(grade)
            else:

                messages.warning(request, 'Alanları Kontrol Ediniz')
                return redirect('sbs:updateProfileCoach')

            if visa_form.is_valid():
                visa = visa_form.save()
                if not coach.visa.all():
                    coach.visa.add(visa)
            else:

                messages.warning(request, 'Alanları Kontrol Ediniz')
                return redirect('sbs:updateProfileCoach')

            messages.success(request, 'Antrenör Bilgileri Başarıyla Güncellenmiştir.')
            return redirect('sbs:updateProfileCoach')

    return render(request, 'TVGFBF/Profile/CoachProfile.html',
                  {'user_form': user_form, 'communication_form': communication_form, 'iban': iban,
                   'person_form': person_form, 'password_form': password_form, 'coach_form': coach_form,
                   'grade_form': grade_form, 'visa_form': visa_form})


@login_required
def updateProfileReferee(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    user = request.user
    referee = Referee.objects.get(person__user=user)
    person = Person.objects.get(pk=referee.person.pk)
    communication = Communication.objects.get(pk=referee.communication.pk)
    user_form = HavaUserForm(request.POST or None, instance=user)
    person_form = PersonForm(request.POST or None, instance=person)
    communication_form = ProfileCommunicationForm(request.POST or None, instance=communication)
    refere_form = RefereeForm(request.POST or None, request.FILES or None, instance=referee)
    password_form = SetPasswordForm(request.user, request.POST)
    iban = referee.person.iban
    if request.method == 'POST':

        if request.POST['save_button'] == 'profile':
            if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid():
                user.username = user_form.cleaned_data['email']
                user.first_name = user_form.cleaned_data['first_name']
                user.last_name = user_form.cleaned_data['last_name']
                user.email = user_form.cleaned_data['email']
                user.save()
                person_form.save(request)
                iban = request.POST['iban']
                person.iban = iban
                person.save()
                communication_form.save(request)
                messages.success(request, 'Profil Bilgileri Başarıyla Güncellenmiştir.')

                return redirect('sbs:updateProfileReferee')
            else:

                messages.warning(request, 'Alanları Kontrol Ediniz')

        elif request.POST['save_button'] == 'password':
            if password_form.is_valid():

                user.set_password(password_form.cleaned_data['new_password1'])
                user.save()

                messages.success(request, 'Şifre Bilgileri Başarıyla Güncellenmiştir.')

                return redirect('sbs:updateProfileReferee')
            else:

                messages.warning(request, 'Alanları Kontrol Ediniz')


        else:
            if refere_form.is_valid():
                refere_form.save()
                messages.success(request, 'Hakem Bilgileri Başarıyla Güncellenmiştir.')

                return redirect('sbs:updateProfileReferee')

            else:

                messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'TVGFBF/Profile/RefereeProfile.html',
                  {'user_form': user_form, 'communication_form': communication_form, 'iban': iban,
                   'person_form': person_form, 'password_form': password_form, 'refere_form': refere_form})


@login_required
def updateProfileClubUser(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    user = request.user
    clubUser = SportClubUser.objects.get(person__user=user)
    person = Person.objects.get(pk=clubUser.person.pk)
    communication = Communication.objects.get(pk=clubUser.communication.pk)
    user_form = HavaUserForm(request.POST or None, instance=user)
    person_form = PersonForm(request.POST or None, instance=person)
    communication_form = ProfileCommunicationForm(request.POST or None, instance=communication)
    password_form = SetPasswordForm(request.user, request.POST)
    iban = clubUser.person.iban
    if request.method == 'POST':

        if request.POST['save_button'] == 'profile':
            if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid():
                user.username = user_form.cleaned_data['email']
                user.first_name = user_form.cleaned_data['first_name']
                user.last_name = user_form.cleaned_data['last_name']
                user.email = user_form.cleaned_data['email']
                user.save()
                person_form.save(request)
                iban = request.POST['iban']
                person.iban = iban
                person.save()
                communication_form.save(request)
                messages.success(request, 'Profil Bilgileri Başarıyla Güncellenmiştir.')

                return redirect('sbs:updateProfileClubUser')
            else:

                messages.warning(request, 'Alanları Kontrol Ediniz')

        elif request.POST['save_button'] == 'password':
            if password_form.is_valid():

                user.set_password(password_form.cleaned_data['new_password1'])
                user.save()

                messages.success(request, 'Şifre Bilgileri Başarıyla Güncellenmiştir.')

                return redirect('sbs:updateProfileClubUser')
            else:

                messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'TVGFBF/Profile/ClubUserProfile.html',
                  {'user_form': user_form, 'communication_form': communication_form, 'iban': iban,
                   'person_form': person_form, 'password_form': password_form, })