import traceback
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.shortcuts import redirect

from sbs.models import Organizer, AirSportsCompetition, EducationSeminar, HavaLevel
from sbs.models.ekabis.EnumFields import EnumFields
from sbs.models.havaspor.HavaLevel import HavaLevel
from sbs.models.ekabis.CategoryItem import CategoryItem
from sbs.models.ekabis.City import City
from sbs.models.ekabis.Communication import Communication
from sbs.models.ekabis.Country import Country
from sbs.models.ekabis.HavaSporAktarim import SystemEbysBranches, SystemEbysBranchesSub, SystemEbysCity, \
    SystemEbysCommonuser, SystemEbysMembershipCoach, SystemEbysMembershipClub, \
    SystemEbysAthleteCoachAppend, SystemEbysRefereeStatu, SystemEbysMembershipReferee, SystemEbysMembershipAthlete, \
    SystemEbysMembershipOrganizer, SystemEbysCompetition, SystemEbysEducationseminar, SystemEbysCoaches
from sbs.models.ekabis.Person import Person
from sbs.models.havaspor.Athlete import Athlete
from sbs.models.havaspor.Branch import Branch
from sbs.models.havaspor.CertificateDegree import CertificateDegree
from sbs.models.havaspor.Club import Club
from sbs.models.havaspor.ClubRole import ClubRole
from sbs.models.havaspor.Coach import Coach
from sbs.models.havaspor.License import License
from sbs.models.havaspor.Referee import Referee
from sbs.models.havaspor.SportClubUser import SportClubUser


def branchTransmission(request):
    branchs = SystemEbysBranches.objects.all()
    for branch in branchs:
        if not Branch.objects.filter(title=branch.title):
            secretId = branch.secret_id
            title = branch.title
            sort = branch.sort
            b = Branch(title=title, sort=sort, secretId=secretId)
            b.save()
    return redirect('sbs:view_admin')


def branchSubTransmission(request):
    branchSubs = SystemEbysBranchesSub.objects.all()
    for branchSub in branchSubs:
        if not Branch.objects.filter(title=branchSub.title):
            branch = SystemEbysBranches.objects.get(secret_id=branchSub.branch_secret_id)
            branchParent = Branch.objects.get(title=branch.title)
            branchSubTitle = branchSub.title
            branchSubParentId = branchParent.id
            branchSubParent = False
            b = Branch(title=branchSubTitle, parent_id=branchSubParentId, is_parent=branchSubParent,
                       secretId=branchSub.secret_id)
            b.save()

    return redirect('sbs:view_admin')


def city(request):
    cities = SystemEbysCity.objects.all()
    for city in cities:
        if not City.objects.filter(name=city.title):
            b = City(name=city.title)
            b.save()
    return redirect('sbs:view_admin')


def country(request):
    b = Country(name='Türkiye')
    b.save()
    return redirect('sbs:view_admin')


def UserTransmission(request):
    try:
        with transaction.atomic():

            commonUser = SystemEbysCommonuser.objects.all()[2100:]
            for user in commonUser:
                if not User.objects.filter(email=user.email):
                    newUser = User(first_name=user.name, last_name=user.surname, username=user.email, email=user.email)
                    password = User.objects.make_random_password()
                    newUser.set_password(password)
                    newUser.is_active = True
                    newUser.save()
                    user_types = user.user_type
                    user_types = user_types.split(',')
                    group = None
                    for type in user_types:
                        if type == '1':
                            group = Group.objects.get(name='Sporcu')

                        elif type == '2':
                            group = Group.objects.get(name='Antrenör')

                        elif type == '3':
                            group = Group.objects.get(name='Hakem')

                        elif type == '4':
                            group = Group.objects.get(name='Organizatör')

                        elif type == '5':
                            group = Group.objects.get(name='Kulüp Yetkilisi')

                        elif type == '6':
                            group = Group.objects.get(name='Uçuş Okulu Yetkilisi')

                        newUser.groups.add(group)
                        newUser.save()

                    gender = user.gender
                    if gender:
                        if gender == 'kadin':
                            gender = 1
                        else:
                            gender = 0
                    if user.phone and user.phone != '':
                        phone = user.phone
                        phone = phone.split(' ')
                        if len(phone) == 4:
                            phone_first = phone[0].split('(')[1].split(')')[0]
                            phone = phone_first + phone[1] + phone[2] + phone[3]
                        else:
                            phone = user.phone

                    havaPerson = Person(tc=user.tckimlik, birthDate=user.birthday,
                                        hesKodu=user.heskodu, user=newUser,
                                        bloodType=user.bloodgroup, gender=gender, secretId=user.secret_id,
                                        iban=user.iban)
                    havaPerson.save()

                    if user.acildurum_phone:
                        acildurum_phone = user.acildurum_phone

                        acildurum_phone = acildurum_phone.split(' ')
                        if len(acildurum_phone) == 4:
                            acildurum_phone_first = acildurum_phone[0].split('(')[1].split(')')[0]
                            acildurum_phone = acildurum_phone_first + acildurum_phone[1] + acildurum_phone[2] + \
                                              acildurum_phone[3]
                        else:
                            acildurum_phone = user.acildurum_phone
                    else:
                        acildurum_phone = '055XXXXXXXX'
                    if user.city == 0:
                        city = None
                    else:
                        city = City.objects.get(id=int(user.city))
                    communication = Communication(phoneNumber=phone, acildurum_phone=acildurum_phone,
                                                  acildurum_kisi=user.acildurum_kisi, address=user.address,
                                                  city=city,
                                                  country=Country.objects.get(name='Türkiye'), secretId=user.secret_id)
                    communication.save()
                else:
                    print(user.email)
            return redirect('sbs:view_admin')
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('sbs:view_admin')


def ClubTransmission(request):
    try:
        with transaction.atomic():
            clubs = SystemEbysMembershipClub.objects.all()
            for club in clubs:
                user = SystemEbysCommonuser.objects.get(secret_id=club.user_secret_id)
                current_user = User.objects.get(email=user.email)
                if Person.objects.filter(secretId=club.user_secret_id) and Communication.objects.filter(
                        secretId=user.secret_id):
                    person = Person.objects.get(secretId=club.user_secret_id)

                    if club.kulupil:
                        city = City.objects.get(pk=int(club.kulupil))
                    else:
                        city = None
                    com = Communication(phoneNumber=club.kuluptelefon, address=club.kulupadres,
                                        country=Country.objects.get(name='Türkiye'),
                                        city=city)
                    com.save()
                    phone = user.phone
                    phone = phone.split(' ')
                    if len(phone) == 4:
                        phone_first = phone[0].split('(')[1].split(')')[0]
                        phone = phone_first + phone[1] + phone[2] + phone[3]
                    else:
                        phone = user.phone

                    communication = Communication.objects.get(secretId=user.secret_id)

                    if not SportClubUser.objects.filter(communication=communication):
                        sportClubUser = SportClubUser(person=person, communication=communication, user=current_user,
                                                      role=ClubRole.objects.get(name='BAŞKAN'))
                        sportClubUser.save()
                        newClub = Club(name=club.kulupadi, clubMail=club.kulupeposta, communication=com,
                                       username=club.kulupeposta, infoLevel=club.infolevel, infoStatus=club.infostatus,
                                       secretId=club.user_secret_id)
                        newClub.save()
                        newClub.clubUser.add(sportClubUser)
                        newClub.save()
                        if club.branch:
                            for item in club.branch.split(','):
                                branch = Branch.objects.get(secretId=item)
                                newClub.branch.add(branch)
                                newClub.save()

                    else:
                        print(current_user.first_name + ' ' + current_user.last_name)
                        print(communication.secretId)
                        print(sportClubUser.pk)
            return redirect('sbs:view_admin')
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        print(user.email)
        return redirect('sbs:view_admin')


def CoachTransmission(request):
    try:
        with transaction.atomic():
            membershipCoachs = SystemEbysMembershipCoach.objects.all()
            for membershipCoach in membershipCoachs:
                if Person.objects.filter(secretId=membershipCoach.user_secret_id) and Communication.objects.filter(
                        secretId=membershipCoach.user_secret_id):
                    personCoach = Person.objects.get(secretId=membershipCoach.user_secret_id)
                    communicatinCoach = Communication.objects.get(secretId=membershipCoach.user_secret_id)
                    coachAdd = Coach(person=personCoach, communication=communicatinCoach,
                                     nufusCuzdani=membershipCoach.nufuscuzdani,
                                     diploma=membershipCoach.diploma, sabikaKaydi=membershipCoach.sabikakaydi,
                                     cezaYazisi=membershipCoach.cezayazisi,
                                     saglikBeyanFormu=membershipCoach.saglikbeyanformu,
                                     antrenorBelgesi=membershipCoach.antrenorbelgesi,
                                     infoLevel=membershipCoach.infolevel, infoStatus=membershipCoach.infostatus)
                    coachAdd.save()
                    if membershipCoach.branch:
                        for item in membershipCoach.branch.split(','):
                            branch = Branch.objects.get(secretId=item)
                            coachAdd.branch.add(branch)
                            coachAdd.save()
            return redirect('sbs:view_admin')

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('sbs:view_admin')


def ClubCoachTransmission(request):
    try:
        with transaction.atomic():
            clubCoaches = SystemEbysAthleteCoachAppend.objects.filter(append_type='coach')
            for clubCoach in clubCoaches:
                isKulup = clubCoach.club_flightscholl_secret_id.split('_')[0]
                if isKulup == 'kulup':
                    if Coach.objects.filter(person__secretId=clubCoach.user_secret_id):
                        coach = Coach.objects.get(person__secretId=clubCoach.user_secret_id)

                        clubUserSecretId = clubCoach.append_user_secret_id
                        club = Club.objects.get(secretId=clubUserSecretId)
                        club.coachs.add(coach)
                        club.save()
                    else:
                        print(clubCoach.user_secret_id)

                else:
                    print('Uçuş Okulu')

            return redirect('sbs:view_admin')

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('sbs:view_admin')


def RefereeStatusTransmission(request):
    try:
        with transaction.atomic():
            status = SystemEbysRefereeStatu.objects.all()
            for statu in status:
                if statu.statu:
                    if CategoryItem.objects.filter(name=statu.statu):
                        currentStatus = CategoryItem.objects.get(name=statu.statu)
                    else:
                        currentStatus = CategoryItem(name=statu.statu, forWhichClazz='REFEREE_GRADE')
                        currentStatus.save()
                refereStatus = HavaLevel(definition=currentStatus, secretId=statu.user_secret_id,
                                         branch=Branch.objects.get(secretId=statu.branch_secret_id),
                                         definitionChangeUser=Person.objects.get(secretId=statu.user_secret_id).user,
                                         modificationDate=statu.statu_change_date, levelType=EnumFields.LEVELTYPE.GRADE)
                refereStatus.save()
                referee = SystemEbysMembershipReferee.objects.get(user_secret_id=statu.user_secret_id)
                if Referee.objects.filter(secretId=referee.user_secret_id):
                    currentReferee = Referee.objects.get(secretId=referee.user_secret_id)
                else:
                    currentReferee = Referee(secretId=referee.user_secret_id, nufusCuzdani=referee.nufuscuzdani,
                                             infoStatus=referee.infostatus, infoLevel=referee.infolevel,
                                             hakemBilgiFormu=referee.hakembilgiformu, cezaYazisi=referee.cezayazisi,
                                             diploma=referee.diploma, saglikBeyanFormu=referee.saglikbeyanformu,
                                             sabikaKaydi=referee.sabikakaydi,
                                             person=Person.objects.get(secretId=referee.user_secret_id),
                                             communication=Communication.objects.get(secretId=referee.user_secret_id))

                    currentReferee.save()
                currentReferee.grades.add(refereStatus)
                currentReferee.save()
                # for item in referee.branch.split(','):
                #     if Branch.objects.filter(secretId=item):
                #         branch = Branch.objects.get(secretId=item)
                #         currentReferee.branch.add(branch)
                #         currentReferee.save()
                #     else:
                #         print(item)
                # secret_array.append(currentReferee.secretId)

        return redirect('sbs:view_admin')
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('sbs:view_admin')


def RefereeTransmission(request):
    try:
        with transaction.atomic():
            referees = SystemEbysMembershipReferee.objects.all()
            secret_array = []
            for referee in referees:
                if not Referee.objects.filter(secretId=referee.user_secret_id):
                    currentReferee = Referee(secretId=referee.user_secret_id, nufusCuzdani=referee.nufuscuzdani,
                                             infoStatus=referee.infostatus, infoLevel=referee.infolevel,
                                             hakemBilgiFormu=referee.hakembilgiformu, cezaYazisi=referee.cezayazisi,
                                             diploma=referee.diploma, saglikBeyanFormu=referee.saglikbeyanformu,
                                             sabikaKaydi=referee.sabikakaydi,
                                             person=Person.objects.get(secretId=referee.user_secret_id),
                                             communication=Communication.objects.get(secretId=referee.user_secret_id))
                    currentReferee.save()
                    for item in referee.branch.split(','):
                        if Branch.objects.filter(secretId=item):
                            branch = Branch.objects.get(secretId=item)
                            currentReferee.branch.add(branch)
                            currentReferee.save()
                        else:
                            print(item)

        return redirect('sbs:view_admin')
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('sbs:view_admin')


def AthleteTransmission(request):
    try:
        with transaction.atomic():
            athletes = SystemEbysMembershipAthlete.objects.all()
            for athlete in athletes:
                if not Athlete.objects.filter(person__secretId=athlete.user_secret_id):
                    newAthlete = Athlete()
                    # print(athlete.user_secret_id)
                    if Person.objects.filter(secretId=athlete.user_secret_id):
                        person = Person.objects.get(secretId=athlete.user_secret_id)
                        person.height = athlete.boy
                        person.weight = athlete.kilo
                        person.save()
                        newAthlete.person = person
                    if Communication.objects.filter(secretId=athlete.user_secret_id):
                        communication = Communication.objects.get(secretId=athlete.user_secret_id)
                        newAthlete.communication = communication
                    license = License(lisansPhoto=athlete.lisansfoto, licenseName=athlete.lisanslar,
                                      expireDate=athlete.lisansgecerlilik, licenseNo=athlete.sporculisansno)

                    license.save()
                    certificate = CertificateDegree(name=athlete.sertifikaderece, educationPlace=athlete.egitimyer)
                    certificate.save()

                    newAthlete.airTribuneId = athlete.airtribune_id
                    newAthlete.insurancePolicy = athlete.sigortapolice
                    newAthlete.insuranceCompany = athlete.sigortasirketi
                    if SystemEbysAthleteCoachAppend.objects.filter(user_secret_id=athlete.user_secret_id):
                        club = SystemEbysAthleteCoachAppend.objects.filter(user_secret_id=athlete.user_secret_id).last()
                        if Club.objects.filter(secretId=club.append_user_secret_id):
                            sportClub = Club.objects.get(secretId=club.append_user_secret_id)
                    else:
                        sportClub = None
                    newAthlete.club = sportClub
                    newAthlete.flightJump = athlete.ucusatlayis
                    newAthlete.successDegree = athlete.basarilariniz
                    newAthlete.last12month = athlete.son12ay
                    newAthlete.totalSortie = athlete.toplamsorti
                    newAthlete.infoLevel = athlete.infolevel
                    newAthlete.infoStatus = athlete.infostatus
                    newAthlete.save()
                    newAthlete.certificateDegree.add(certificate)
                    # print(athlete.branch)
                    if athlete.branch:
                        for item in athlete.branch.split(','):
                            # print(item)
                            branch = Branch.objects.get(secretId=item)
                            newAthlete.branch.add(branch)
                    newAthlete.licenses.add(license)
                    newAthlete.save()

        return redirect('sbs:view_admin')

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('sbs:view_admin')


def deleteClub(request):
    clubs = SportClubUser.objects.all()
    for x in clubs:
        x.delete()
        print(' ..delete !!')
    return redirect('sbs:view_admin')


def test(request):
    print('Git deneme ')
    pass


def OrganizerTransmission(request):
    try:
        with transaction.atomic():
            organizers = SystemEbysMembershipOrganizer.objects.all()

            for organizer in organizers:
                if not Organizer.objects.filter(person__secretId=organizer.user_secret_id):
                    if organizer.firmatelefon and organizer.firmatelefon != '':
                        companyPhone = organizer.firmatelefon
                        companyPhone = companyPhone.split(' ')
                        if len(companyPhone) == 4:
                            companyPhone_first = companyPhone[0].split('(')[1].split(')')[0]
                            companyPhone = companyPhone_first + companyPhone[1] + companyPhone[2] + companyPhone[3]
                        else:
                            companyPhone = organizer.firmatelefon
                    else:
                        companyPhone = None
                    currentOrganizer = Organizer(person=Person.objects.get(secretId=organizer.user_secret_id),
                                                 communication=Communication.objects.get(
                                                     secretId=organizer.user_secret_id),
                                                 companyName=organizer.firmaunvani,
                                                 companyRepresentative=organizer.firmayetkilisi,
                                                 companyTaxOffice=organizer.firmavdaire,
                                                 companyTaxNumber=organizer.firmavno,
                                                 companyPhoneNumber=companyPhone,
                                                 companyEmail=organizer.firmatelefon,
                                                 companyAddress=organizer.firmaadres,
                                                 infoStatus=organizer.infostatus, infoLevel=organizer.infolevel)
                    currentOrganizer.save()
                    for item in organizer.branch.split(','):
                        if Branch.objects.filter(secretId=item):
                            branch = Branch.objects.get(secretId=item)
                            currentOrganizer.branch.add(branch)
                            currentOrganizer.save()
                        else:
                            print(item)

        return redirect('sbs:view_admin')
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('sbs:view_admin')


def AirSportsCompetitionTransmission(request):
    try:
        with transaction.atomic():
            competitions = SystemEbysCompetition.objects.all()

            for competition in competitions:
                if not AirSportsCompetition.objects.filter(secretId=competition.secret_id):
                    competitionCreator = Person.objects.get(secretId=competition.creator).user
                    currentAirSportsCompetition = AirSportsCompetition(secretId=competition.secret_id,
                                                                       name=competition.title,
                                                                       city=City.objects.get(id=int(competition.city)),
                                                                       startDate=datetime.strptime(
                                                                           competition.start_date, "%d.%m.%Y").strftime(
                                                                           '%Y-%m-%d'),
                                                                       finishDate=datetime.strptime(
                                                                           competition.finish_date,
                                                                           "%d.%m.%Y").strftime('%Y-%m-%d'),
                                                                       description=competition.description,
                                                                       creator=competitionCreator,
                                                                       createdDate=competition.created_date,
                                                                       status=competition.status)
                    currentAirSportsCompetition.save()
                    if competition.category_secret:
                        for item in competition.category_secret.split(','):
                            if Branch.objects.filter(secretId=item):
                                branch = Branch.objects.get(secretId=item)
                                currentAirSportsCompetition.branch.add(branch)
                                currentAirSportsCompetition.save()
                            else:
                                print(item)
        return redirect('sbs:view_admin')
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('sbs:view_admin')


def CoachTransmission2(request):  # system_ebys_coaches
    try:
        with transaction.atomic():
            membershipCoachs = SystemEbysCoaches.objects.all()
            for membershipCoach in membershipCoachs:
                if not User.objects.filter(username=membershipCoach.email):
                    name = membershipCoach.namesurname.split()
                    if len(name) == 2:
                        firstName = name[0]
                        lastName = name[1]
                    else:
                        firstName = name[0] + ' ' + name[1]
                        lastName = name[2]
                    coachUser = User(first_name=firstName, last_name=lastName, username=membershipCoach.email,
                                     email=membershipCoach.email)
                    password = User.objects.make_random_password()
                    coachUser.set_password(password)
                    coachUser.is_active = True
                    coachUser.save()
                    group = Group.objects.get(name='Antrenör')
                    coachUser.groups.add(group)
                    coachUser.save()

                    gender = 0
                    if membershipCoach.phone and membershipCoach.phone != '':
                        phone = membershipCoach.phone
                        phone = phone.split(' ')
                        if len(phone) == 4:
                            phone = phone[0] + phone[1] + phone[2] + phone[3]
                        else:
                            phone = membershipCoach.phone

                    coachPerson = Person(tc=membershipCoach.tckimlik,
                                         birthDate=datetime.strptime(membershipCoach.birthday, "%d.%m.%Y").strftime(
                                             '%Y-%m-%d'), user=coachUser, gender=gender,
                                         secretId=membershipCoach.secret_id,
                                         iban=membershipCoach.iban)
                    coachPerson.save()

                    if membershipCoach.city == 0:
                        city = None
                    else:
                        city = City.objects.get(id=int(membershipCoach.city))
                    coachCommunication = Communication(phoneNumber=phone,
                                                       address=membershipCoach.address,
                                                       city=city,
                                                       country=Country.objects.get(name='Türkiye'),
                                                       secretId=membershipCoach.secret_id)
                    coachCommunication.save()

                    if Person.objects.filter(secretId=membershipCoach.secret_id) and Communication.objects.filter(
                            secretId=membershipCoach.secret_id):
                        personCoach = Person.objects.get(secretId=membershipCoach.secret_id)
                        communicatinCoach = Communication.objects.get(secretId=membershipCoach.secret_id)
                        coachAdd = Coach(person=personCoach, communication=communicatinCoach,
                                         infoStatus=membershipCoach.status)
                        coachAdd.save()
                        if membershipCoach.branches:
                            for item in membershipCoach.branches.split(','):
                                branch = Branch.objects.get(secretId=item)
                                coachAdd.branch.add(branch)
                                coachAdd.save()
            return redirect('sbs:view_admin')

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('sbs:view_admin')


def EducationSeminarTransmission(request):
    try:
        with transaction.atomic():
            educationSeminars = SystemEbysEducationseminar.objects.all()

            for educationSeminar in educationSeminars:
                if not EducationSeminar.objects.filter(secretId=educationSeminar.secret_id):
                    educationSeminarCreator = Person.objects.get(secretId=educationSeminar.creator).user
                    currentEducationSeminar = EducationSeminar(secretId=educationSeminar.secret_id,
                                                               name=educationSeminar.title,
                                                               city=City.objects.get(id=int(educationSeminar.city)),
                                                               startDate=datetime.strptime(
                                                                   educationSeminar.start_date, "%d.%m.%Y").strftime(
                                                                   '%Y-%m-%d'),
                                                               finishDate=datetime.strptime(
                                                                   educationSeminar.finish_date,
                                                                   "%d.%m.%Y").strftime('%Y-%m-%d'),
                                                               description=educationSeminar.description,
                                                               creator=educationSeminarCreator,
                                                               createdDate=educationSeminar.created_date,
                                                               status=educationSeminar.status,
                                                               educationTime=educationSeminar.edu_time)
                    currentEducationSeminar.save()
                    if educationSeminar.branch:
                        for item in educationSeminar.branch.split(','):
                            if Branch.objects.filter(secretId=item):
                                branch = Branch.objects.get(secretId=item)
                                currentEducationSeminar.branch.add(branch)
                                currentEducationSeminar.save()
                            else:
                                print(item)
                    if educationSeminar.coaches:
                        for educationCoach in educationSeminar.coaches.split(','):
                            if Coach.objects.filter(person__secretId=educationCoach):
                                currentEducationSeminarCoach = Coach.objects.get(person__secretId=educationCoach)
                                currentEducationSeminar.coaches.add(currentEducationSeminarCoach)
                                currentEducationSeminar.save()
                            else:
                                print(item)
        return redirect('sbs:view_admin')
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('sbs:view_admin')
