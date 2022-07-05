# from django.contrib.auth import logout
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User, Group
# from django.shortcuts import redirect
#
# from sbs.models import *
# from sbs.models.FedsportalModels import Sporcular, Turnuvalar, TurnSporculari, TurnHakemleri, TurnSporcuAntrenorleri, \
#     TurnKategorileri, Malzemeler, MalzHareket, Vizeler
# from sbs.models.EnumFields import EnumFields
# from sbs.models.Material import Material
# from sbs.services import general_methods
#
# from sbs.models.CompetitionsAthlete import CompetitionsAthlete
#
# from sbs.models.Category import Category
# from sbs.models.Deposit import Deposit
# from sbs.models.CompetitionCoach import CompetitionCoach
#
# from datetime import date, datetime
#
# from sbs.models.Products import Products
#
#
#
# @login_required
# def kulup_aktar(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#
#     eskikulupler=FedsportalModels.Kulupler.objects.all()
#     for e in eskikulupler :
#         citya = City.objects.get(pk=e.ilid.pk)
#         country=Country.objects.get(pk=1)
#         c = Communication(address=e.adres1,phoneNumber=e.telefon,city=citya,country=country)
#         c.save()
#         s = SportsClub(pk=e.kulupid,name=e.kulupadi,foundingDate=e.tesciltarihi,clubMail=e.eposta,communication=c)
#
#         s.save()
#
# @login_required
# def hakem_aktar(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#
#     eskihakemler = Sporcular.objects.filter(hakem=1)
#     # print(eskihakemler.count())
#     for e in eskihakemler :
#         # print(e.adi + " " + e.soyadi)
#         user = User(
#             first_name=e.adi,
#             last_name=e.soyadi,
#             email=e.eposta if e.eposta else 'badminton@hotmail.com',
#             username=e.tcno
#
#                     )
#         user.save()
#
#         # print(user)
#         grup = Group.objects.get(name='Hakem')
#         user.groups.add(grup)
#         # print(grup)
#         meterial = Meterial(ayakkabi=e.ayakkabi,
#                             esofman=e.esofman,
#                             tshirt=e.tshirt,
#                             raket=e.raket
#                             )
#         meterial.save()
#         # print(meterial)
#         # print(e.egitimid)
#         person = Person(
#             tc=e.tcno,
#             birthplace=e.dogumyeri,
#             motherName=e.anneadi,
#             fatherName=e.babaadi,
#             birthDate=e.dogumtarihi,
#             bloodType=e.kangrubu,
#             # profileImage=e.resim,
#             gender=e.cinsiyet,
#             uyrukid=e.uyrukid,
#             nufus_ailesirano=e.nufus_ailesirano,
#             nufus_ciltno=e.nufus_ciltno,
#             nufus_sirano=e.nufus_sirano,
#             meslek=e.meslek,
#             kurum=e.kurum,
#             is_unvani=e.is_unvani,
#             # meterial=meterial.id,
#             # education=e.egitimid
#
#         )
#
#         # print(person)
#         person.material = meterial
#         person.save()
#
#         comikamet = Communication(
#             phoneNumber=e.ceptel,
#             address=e.yerlesimyeri,
#             city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
#             country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
#         )
#         comikamet.save()
#         comev = Communication(
#             phoneNumber=e.ceptel,
#             phoneNumber2=e.evtel,
#             address=e.ev_adresi,
#             city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
#             country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
#         )
#         comev.save()
#         comis = Communication(
#             phoneNumber=e.ceptel,
#             phoneNumber2=e.istel,
#             address=e.is_adresi,
#             city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
#             country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
#         )
#         comis.save()
#         # print(comikamet)
#         # print(comev)
#         # print(comis)
#         hakem = Judge(
#             pk=e.sporcuid,
#             person=person,
#             communication=comikamet,
#             communicationHome=comev,
#             communicationJop=comis,
#             user=user,
#             iban=e.bankahesapno,
#             oldpk=e.sporcuid
#         )
#         hakem.save()
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def antrenor_aktar(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#
#     eskihakemler = Sporcular.objects.filter(sporcuid=89).exclude(tcno=None)
#     # print(eskihakemler.count())
#
#     grup = Group.objects.get(name='Antrenor')
#     # print(grup)
#     for e in eskihakemler:
#         print(e.adi + " " + e.soyadi)
#         if User.objects.filter(username=e.tcno):
#             if User.objects.filter(username=e.tcno)[0].groups.filter(name="Hakem"):
#                 if not (Coach.objects.filter(user=User.objects.filter(username=e.tcno)[0])):
#                     print('if ')
#                     judge = Judge.objects.get(user=User.objects.filter(username=e.tcno)[0])
#                     user = judge.user
#                     coach = Coach(
#                         user=judge.user,
#                         communication=judge.communication,
#                         communicationHome=judge.communicationHome,
#                         communicationJop=judge.communicationJop,
#                         iban=judge.iban,
#                         oldpk=judge.oldpk,
#                         person=judge.person
#
#                     )
#                     coach.save()
#                     coach.user.groups.add(grup)
#                     coach.save()
#                 else:
#                     print('deger eklenmiş')
#
#
#         else:
#             print('eklendi')
#             user = User(
#                 first_name=e.adi,
#                 last_name=e.soyadi,
#                 email=e.eposta if e.eposta else 'badminton@hotmail.com',
#                 username=e.tcno
#
#             )
#             user.save()
#
#             # print(user)
#             user.groups.add(grup)
#             # print(grup)
#             meterial = Material(ayakkabi=e.ayakkabi,
#                                 esofman=e.esofman,
#                                 tshirt=e.tshirt,
#                                 raket=e.raket
#                                 )
#             meterial.save()
#             # print(meterial)
#             # print(e.egitimid)
#             person = Person(
#                 tc=e.tcno,
#                 birthplace=e.dogumyeri,
#                 motherName=e.anneadi,
#                 fatherName=e.babaadi,
#                 birthDate=e.dogumtarihi,
#                 bloodType=e.kangrubu,
#                 # profileImage=e.resim,
#                 gender=e.cinsiyet,
#                 uyrukid=e.uyrukid,
#                 nufus_ailesirano=e.nufus_ailesirano,
#                 nufus_ciltno=e.nufus_ciltno,
#                 nufus_sirano=e.nufus_sirano,
#                 meslek=e.meslek,
#                 kurum=e.kurum,
#                 is_unvani=e.is_unvani,
#                 # meterial=meterial.id,
#                 # education=e.egitimid
#
#             )
#
#             person.material = meterial
#             person.save()
#             # print(person)
#
#             comikamet = Communication(
#                 phoneNumber=e.ceptel,
#                 address=e.yerlesimyeri,
#                 city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
#                 country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
#             )
#             comikamet.save()
#             comev = Communication(
#                 phoneNumber=e.ceptel,
#                 phoneNumber2=e.evtel,
#                 address=e.ev_adresi,
#                 city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
#                 country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
#             )
#             comev.save()
#             comis = Communication(
#                 phoneNumber=e.ceptel,
#                 phoneNumber2=e.istel,
#                 address=e.is_adresi,
#                 city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
#                 country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
#             )
#             comis.save()
#             # print(comikamet)
#             # print(comev)
#             # print(comis)
#             coach = Coach(
#                 pk=e.sporcuid,
#                 person=person,
#                 communication=comikamet,
#                 communicationHome=comev,
#                 communicationJop=comis,
#                 user=user,
#                 iban=e.bankahesapno,
#                 oldpk=e.sporcuid
#             )
#             coach.save()
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def sporcu_aktar(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#
#     eskihakemler = Sporcular.objects.filter(sporcu=1).exclude(tcno=None)
#     print(eskihakemler.count())
#
#     # grup = Group.objects.get(name='Sporcu')
#     # print(grup)
#     # for e in eskihakemler:
#     #
#     #     if User.objects.filter(username=e.tcno):
#     #         if User.objects.filter(username=e.tcno)[0].groups.filter(name="Hakem"):
#     #             if not (Athlete.objects.filter(user=User.objects.filter(username=e.tcno)[0])):
#     #                 judge = Judge.objects.get(user=User.objects.filter(username=e.tcno)[0])
#     #                 print(e.adi + " " + e.soyadi)
#     #                 athlete = Athlete(
#     #                     user=judge.user,
#     #                     communication=judge.communication,
#     #                     communicationHome=judge.communicationHome,
#     #                     communicationJop=judge.communicationJop,
#     #                     iban=judge.iban,
#     #                     oldpk=judge.oldpk,
#     #                     person=judge.person
#     #
#     #                 )
#     #                 athlete.save()
#     #                 athlete.user.groups.add(grup)
#     #                 athlete.save()
#     #             else:
#     #                 print('Control Hakem')
#     #         elif User.objects.filter(username=e.tcno)[0].groups.filter(name="Antrenor"):
#     #             if not (Athlete.objects.filter(user=User.objects.filter(username=e.tcno)[0])):
#     #                 coach = Coach.objects.get(user=User.objects.filter(username=e.tcno)[0])
#     #                 athlete = Athlete(
#     #                     user=coach.user,
#     #                     communication=coach.communication,
#     #                     communicationHome=coach.communicationHome,
#     #                     communicationJop=coach.communicationJop,
#     #                     iban=coach.iban,
#     #                     oldpk=coach.oldpk,
#     #                     person=coach.person
#     #
#     #                 )
#     #                 athlete.save()
#     #                 athlete.user.groups.add(grup)
#     #                 athlete.save()
#     #             else:
#     #                 print('Control Antrenor')
#     #
#     #
#     #
#     #     else:
#     #         user = User(
#     #             first_name=e.adi,
#     #             last_name=e.soyadi,
#     #             email=e.eposta if e.eposta else 'badminton@hotmail.com',
#     #             username=e.tcno
#     #
#     #         )
#     #         user.save()
#     #
#     #         # print(user)
#     #         user.groups.add(grup)
#     #         # print(grup)
#     #         meterial = Meterial(ayakkabi=e.ayakkabi,
#     #                             esofman=e.esofman,
#     #                             tshirt=e.tshirt,
#     #                             raket=e.raket
#     #                             )
#     #         meterial.save()
#     #         # print(meterial)
#     #         # print(e.egitimid)
#     #         person = Person(
#     #             tc=e.tcno,
#     #             birthplace=e.dogumyeri,
#     #             motherName=e.anneadi,
#     #             fatherName=e.babaadi,
#     #             birthDate=e.dogumtarihi,
#     #             bloodType=e.kangrubu,
#     #             # profileImage=e.resim,
#     #             gender=e.cinsiyet,
#     #             uyrukid=e.uyrukid,
#     #             nufus_ailesirano=e.nufus_ailesirano,
#     #             nufus_ciltno=e.nufus_ciltno,
#     #             nufus_sirano=e.nufus_sirano,
#     #             meslek=e.meslek,
#     #             kurum=e.kurum,
#     #             is_unvani=e.is_unvani,
#     #             # meterial=meterial.id,
#     #             # education=e.egitimid
#     #
#     #         )
#     #
#     #         person.material = meterial
#     #         person.save()
#     #         # print(person)
#     #
#     #         comikamet = Communication(
#     #             phoneNumber=e.ceptel,
#     #             address=e.yerlesimyeri,
#     #             city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
#     #             country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
#     #         )
#     #         comikamet.save()
#     #         comev = Communication(
#     #             phoneNumber=e.ceptel,
#     #             phoneNumber2=e.evtel,
#     #             address=e.ev_adresi,
#     #             city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
#     #             country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
#     #         )
#     #         comev.save()
#     #         comis = Communication(
#     #             phoneNumber=e.ceptel,
#     #             phoneNumber2=e.istel,
#     #             address=e.is_adresi,
#     #             city=City.objects.filter(name__icontains=e.nufus_ilid.iladi)[0] if e.nufus_ilid else None,
#     #             country=Country.objects.filter(name__icontains="TÜRKİYE")[0],
#     #         )
#     #         comis.save()
#     #         # print(comikamet)
#     #         # print(comev)
#     #         # print(comis)
#     #         athlete = Athlete(
#     #             pk=e.sporcuid,
#     #             person=person,
#     #             communication=comikamet,
#     #             communicationHome=comev,
#     #             communicationJop=comis,
#     #             user=user,
#     #             iban=e.bankahesapno,
#     #             oldpk=e.sporcuid
#     #         )
#     #         athlete.save()
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def lisans_aktar(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#
#     eskihakemler = Sporcular.objects.exclude(kulupid=None).exclude(tcno=None).filter(sporcu=1)
#     print(eskihakemler.count())
#     for item in eskihakemler:
#
#         athlete = Athlete.objects.get(oldpk=item.sporcuid)
#         if athlete.licenses.count() == 0:
#             lisans = License(
#
#                 licenseNo=item.lisansno,
#                 branch=EnumFields.BADMİNTON.value,
#                 isActive=True,
#                 status=License.APPROVED
#             )
#             if item.lisanstarihi is not None:
#                 lisans.expireDate = item.lisanstarihi
#                 lisans.startDate = date(int(item.lisanstarihi.year) - 1, item.lisanstarihi.month, item.lisanstarihi.day)
#
#             if item.kulupid is not None:
#                 lisans.sportsClub = SportsClub.objects.get(pk=item.kulupid.pk)
#             if item.antrenorid is not None:
#                 if Coach.objects.filter(oldpk=item.antrenorid.pk):
#                     lisans.coach = Coach.objects.get(oldpk=item.antrenorid.pk)
#             if item.antrenorid2 is not None:
#                 if Coach.objects.filter(oldpk=item.antrenorid2.pk):
#                     lisans.coach2 = Coach.objects.get(oldpk=item.antrenorid2.pk)
#             lisans.save()
#             athlete.licenses.add(lisans);
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def control(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#     print(Sporcular.objects.filter(sporcu=1).exclude(kulupid=None).exclude(tcno=None).count())
#     for item in Sporcular.objects.filter(sporcu=1).exclude(kulupid=None).exclude(tcno=None):
#         athlete = Athlete.objects.get(oldpk=item.sporcuid)
#         if athlete.licenses.count() > 1:
#             print(item.adi + " " + item.soyadi)
#             for lisans in athlete.licenses.all():
#
#                 athlete.licenses.remove(lisans)
#                 lisans.delete()
#                 if athlete.licenses.count() == 1:
#                     break;
#
#         elif athlete.licenses.count() == 0:
#             print(item.adi + "---" + item.soyadi)
#             lisans = License(
#
#                 licenseNo=item.lisansno,
#                 branch=EnumFields.BADMİNTON.value,
#                 isActive=True,
#                 status=License.APPROVED
#             )
#             if item.lisanstarihi is not None:
#                 lisans.expireDate = item.lisanstarihi
#                 lisans.startDate = date(int(item.lisanstarihi.year) - 1, item.lisanstarihi.month, item.lisanstarihi.day)
#
#             if item.kulupid is not None:
#                 lisans.sportsClub = SportsClub.objects.get(pk=item.kulupid.pk)
#             if item.antrenorid is not None:
#                 if Coach.objects.filter(oldpk=item.antrenorid.pk):
#                     lisans.coach = Coach.objects.get(oldpk=item.antrenorid.pk)
#             if item.antrenorid2 is not None:
#                 if Coach.objects.filter(oldpk=item.antrenorid2.pk):
#                     lisans.coach2 = Coach.objects.get(oldpk=item.antrenorid2.pk)
#             lisans.save()
#             athlete.licenses.add(lisans);
#             athlete.save()
#
#
#
#
#
#
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def kademe_aktar(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#
#     antrenor = Sporcular.objects.exclude(tcno=None).filter(antrenor=1)
#
#     for item in antrenor:
#
#         coach = Coach.objects.get(oldpk=item.sporcuid)
#
#         print(coach.user.get_full_name())
#         print(item.antrenorkademeid)
#         print(item.antrenorvize)
#
#         if item.antrenorkademeid:
#             grade = Level(definition=CategoryItem.objects.get(name=item.antrenorkademeid),
#                           branch=EnumFields.BADMİNTON.value)
#             grade.levelType = EnumFields.LEVELTYPE.GRADE
#             grade.status = Level.APPROVED
#             grade.save()
#             coach.grades.add(grade)
#             coach.save()
#
#         if item.antrenorvize:
#             visa = Level(branch=EnumFields.BADMİNTON.value)
#             visa.startDate = item.antrenorvize
#             visa.definition = CategoryItem.objects.get(forWhichClazz='VISA')
#             visa.levelType = EnumFields.LEVELTYPE.VISA
#             visa.status = Level.APPROVED
#             visa.isActive = True
#             visa.save()
#             coach.visa.add(visa)
#             coach.save()
#
#
#
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def username_aktar(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#
#     users = User.objects.all()
#     for item in users:
#         if item.email != "badminton@hotmail.com":
#             if not User.objects.filter(username=item.email):
#                 if item.username != item.email:
#                     item.username = item.email
#                     item.save()
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def musabaka_aktar(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#
#     competities = Turnuvalar.objects.all()
#
#     for item in competities:
#         print(item.turnuvaadi)
#
#         competi = Competition(
#
#             pk=item.turnuvaid,
#             name=item.turnuvaadi,
#             startDate=item.basltarihi,
#             finishDate=item.bitistarihi,
#             registerStartDate=item.basvurubasltarihi,
#             registerFinishDate=item.basvurubitistarihi,
#             explanation=item.aciklama
#
#         )
#         competi.save()
#
#     print(competities.count())
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def musabaka_sporcu_aktar(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#
#     turn = TurnSporculari.objects.all()
#
#     for item in turn:
#
#         com = CompetitionsAthlete(pk=item.turnsporcuid)
#
#         if not CompetitionsAthlete.objects.filter(pk=item.turnsporcuid):
#             if item.antrenorid:
#                 com.coach = Coach.objects.get(oldpk=item.antrenorid)
#             if item.kulupid:
#                 com.club = SportsClub.objects.get(pk=item.kulupid)
#             if item.sporcuid:
#                 com.athlete = Athlete.objects.get(oldpk=item.sporcuid.pk)
#             if item.turnuvaid:
#                 com.competition = Competition.objects.get(pk=item.turnuvaid.pk)
#             if item.kategoriid:
#                 com.category = Category.objects.get(pk=item.kategoriid.pk)
#             if item.sira:
#                 com.sira = item.sira
#             if item.grupid:
#                 com.grupid = item.grupid
#
#             com.save()
#
#     print(com.count())
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def musabaka_antrenor_aktar(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#
#     coachs = TurnSporcuAntrenorleri.objects.all()
#     print(coachs.count())
#
#     for item in coachs:
#
#         com = CompetitionCoach(pk=item.turnsporcuid)
#         com.pk = item.turnsporcuantrenorid
#
#         if not CompetitionCoach.objects.filter(pk=com.pk):
#
#             if item.turnsporcuid:
#                 com.athlete = Athlete.objects.get(oldpk=item.turnsporcuid.sporcuid.pk)
#             if item.antrenorid:
#                 com.coach = Coach.objects.get(oldpk=item.antrenorid.sporcuid)
#             if item.sira:
#                 com.sira = item.sira
#
#             com.save()
#
#             #
#             # try:
#             #
#             #
#             # except:
#             #     print(item.turnsporcuantrenorid)
#
#     print(coachs.count())
#     return redirect('sbs:admin')
#
#
# @login_required
# def musabaka_hakem_aktar(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#
#     turn = TurnHakemleri.objects.all()
#
#     for item in turn:
#         com = Competition.objects.get(pk=item.turnuvaid.turnuvaid)
#         judge = Judge.objects.get(oldpk=item.hakemid.sporcuid)
#
#         com.judges.add(judge)
#         com.save()
#
#     print(turn.count())
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def musabaka_kademe_aktar(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#
#     turn = TurnKategorileri.objects.all()
#
#     for item in turn:
#         com = Competition.objects.get(pk=item.turnuvaid.turnuvaid)
#         category = Category.objects.get(pk=item.kategoriid.kategoriid)
#
#         com.categoryies.add(category)
#         com.save()
#
#     print(com.count())
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def control2(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#
#     athletes = Athlete.objects.all()
#
#     for item in athletes:
#         if not Sporcular.objects.filter(sporcuid=item.oldpk):
#             print(item.oldpk)
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def mazeme_aktar(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#
#     product = Malzemeler.objects.all()
#
#     for item in product:
#         product = Products(
#             pk=item.malzemeid,
#             name=item.malzemeadi
#
#         )
#         if item.aciklama:
#             product.description = item.aciklama
#
#         if item.kategori == 'Raket':
#             product.category == Products.RAKET
#         if item.kategori == 'Raket Aksesuar':
#             product.category == Products.AKSESUAR
#         if item.kategori == 'Raket Germe':
#             product.category = Products.KORDAJ
#         if item.kategori == 'Raketler':
#             product.category == Products.RAKET
#         if item.kategori == 'Saha Gereçleri':
#             product.category = Products.EKİPMAN
#         if item.kategori == 'Tişört':
#             product.category = Products.KIYAFET
#         if item.kategori == 'TOP' or item.kategori == 'Toplar':
#             product.category == Products.TOPLAR
#         if item.kategori == 'Çanta':
#             product.category == Products.CANTA
#         if item.kategori == 'Şort':
#             product.category == Products.KIYAFET
#         if item.kategori == 'Ayakkabı':
#             product.category == Products.AYAKKABI
#         if item.kategori == 'KİTAP':
#             product.category == Products.KITAP
#         if item.kategori == 'Eşofman':
#             product.category == Products.KIYAFET
#         product.save()
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def comminacations_aktar(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#
#     users = User.objects.all()
#     print(users.count())
#
#     for user in users:
#         if user.groups.filter(name='Antrenor').exists():
#             if Coach.objects.filter(user=user):
#                 athlete = Coach.objects.get(user=user)
#                 athlete.communication.phoneHome = athlete.communicationHome.phoneNumber2
#                 athlete.communication.addressHome = athlete.communicationHome.address
#                 athlete.communication.phoneJop = athlete.communicationJop.phoneNumber2
#                 athlete.communication.addressJop = athlete.communicationJop.address
#                 athlete.communication.save()
#
#
#
#         elif user.groups.filter(name='Hakem').exists():
#             if Judge.objects.filter(user=user):
#                 athlete = Judge.objects.get(user=user)
#                 athlete.communication.phoneHome = athlete.communicationHome.phoneNumber2
#                 athlete.communication.addressHome = athlete.communicationHome.address
#                 athlete.communication.phoneJop = athlete.communicationJop.phoneNumber2
#                 athlete.communication.addressJop = athlete.communicationJop.address
#                 athlete.communication.save()
#
#
#
#
#         elif user.groups.filter(name='Sporcu').exists():
#             if Athlete.objects.filter(user=user):
#                 athlete = Athlete.objects.get(user=user)
#                 athlete.communication.phoneHome = athlete.communicationHome.phoneNumber2
#                 athlete.communication.addressHome = athlete.communicationHome.address
#                 athlete.communication.phoneJop = athlete.communicationJop.phoneNumber2
#                 athlete.communication.addressJop = athlete.communicationJop.address
#                 athlete.communication.save()
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def SporcuControl(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#     sayi = 0
#     athletes = Athlete.objects.all()
#     print(athletes.count())
#     for item in athletes:
#
#         if Sporcular.objects.filter(sporcuid=item.oldpk, sporcu=1):
#             sayi = sayi + 1
#         else:
#
#             item.delete()
#             print(item)
#     print(sayi)
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def AntenorControl(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#     sayi = 0
#     athletes = Coach.objects.all()
#     print(athletes.count())
#     for item in athletes:
#
#         if Sporcular.objects.filter(sporcuid=item.oldpk, sporcu=0):
#
#             for group in item.user.groups.all():
#
#                 if group.name == "Sporcu":
#                     print(item)
#                     item.user.groups.remove(group)
#                     sayi = sayi + 1
#
#     print(sayi)
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def TcnoControl(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#     sayi = 0
#     athletes = Athlete.objects.all()
#     print(athletes.count())
#     for item in athletes:
#
#         if Sporcular.objects.get(sporcuid=item.oldpk):
#             if item.person.tc != Sporcular.objects.get(sporcuid=item.oldpk).tcno:
#                 print(item)
#                 e = Sporcular.objects.get(sporcuid=item.oldpk)
#                 person = Person(
#                     tc=e.tcno,
#                     birthplace=e.dogumyeri,
#                     motherName=e.anneadi,
#                     fatherName=e.babaadi,
#                     birthDate=e.dogumtarihi,
#                     bloodType=e.kangrubu,
#                     # profileImage=e.resim,
#                     gender=e.cinsiyet,
#                     uyrukid=e.uyrukid,
#                     nufus_ailesirano=e.nufus_ailesirano,
#                     nufus_ciltno=e.nufus_ciltno,
#                     nufus_sirano=e.nufus_sirano,
#                     meslek=e.meslek,
#                     kurum=e.kurum,
#                     is_unvani=e.is_unvani,
#                     # meterial=meterial.id,
#                     # education=e.egitimid
#
#                 )
#                 person.save()
#                 item.person = person
#                 item.save()
#                 sayi += 1
#
#     print(sayi)
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def KangrubuSporcu(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#     sayi = 0
#     athletes = Athlete.objects.all()
#     print(athletes.count())
#     for item in athletes:
#
#         if Sporcular.objects.filter(sporcuid=item.oldpk):
#             if item.person.tc != Sporcular.objects.get(sporcuid=item.oldpk).tcno:
#                 print(item)
#                 e = Sporcular.objects.get(sporcuid=item.oldpk)
#                 person = Person(
#                     tc=e.tcno,
#                     birthplace=e.dogumyeri,
#                     motherName=e.anneadi,
#                     fatherName=e.babaadi,
#                     birthDate=e.dogumtarihi,
#                     bloodType=e.kangrubu,
#                     # profileImage=e.resim,
#                     gender=e.cinsiyet,
#                     uyrukid=e.uyrukid,
#                     nufus_ailesirano=e.nufus_ailesirano,
#                     nufus_ciltno=e.nufus_ciltno,
#                     nufus_sirano=e.nufus_sirano,
#                     meslek=e.meslek,
#                     kurum=e.kurum,
#                     is_unvani=e.is_unvani,
#                     # meterial=meterial.id,
#                     # education=e.egitimid
#
#                 )
#                 person.save()
#                 item.person = person
#                 item.save()
#                 sayi += 1
#             else:
#                 if Sporcular.objects.get(sporcuid=item.oldpk).kangrubu:
#                     sporcu = Sporcular.objects.get(sporcuid=item.oldpk).kangrubu
#                     if sporcu == "A(+)":
#                         item.person.bloodType = Person.A1
#                         item.save()
#                     elif sporcu == "AB(+)":
#                         item.person.bloodType = Person.AB1
#                         item.save()
#                     elif sporcu == "0(+)":
#                         item.person.bloodType = Person.O1
#                         item.save()
#                     elif sporcu == "B(+)":
#                         item.person.bloodType = Person.B1
#                         item.save()
#                     elif sporcu == "B(-)":
#                         item.person.bloodType = Person.B2
#                         item.save()
#                     elif sporcu == "0(-)":
#                         item.person.bloodType = Person.O2
#                         item.save()
#                     elif sporcu == "A(-)":
#                         item.person.bloodType = Person.A2
#                         item.save()
#                     elif sporcu == "AB(-)":
#                         item.person.bloodType = Person.AB2
#                         item.save()
#
#     print(sayi)
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def KangrubuAntrenor(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#     sayi = 0
#     test = Coach.objects.exclude(person__bloodType=None)
#     print(test.count())
#     athletes = Coach.objects.all()
#     print(athletes.count())
#     for item in athletes:
#
#         if Coach.objects.filter(oldpk=item.oldpk):
#             if item.person.tc != Sporcular.objects.get(sporcuid=item.oldpk).tcno:
#                 print(item)
#
#                 if Coach.objects.filter(oldpk=item.oldpk):
#                     e = Coach.objects.get(oldpk=item.oldpk)
#                     person = Person(
#                         tc=e.tcno,
#                         birthplace=e.dogumyeri,
#                         motherName=e.anneadi,
#                         fatherName=e.babaadi,
#                         birthDate=e.dogumtarihi,
#                         bloodType=e.kangrubu,
#                         # profileImage=e.resim,
#                         gender=e.cinsiyet,
#                         uyrukid=e.uyrukid,
#                         nufus_ailesirano=e.nufus_ailesirano,
#                         nufus_ciltno=e.nufus_ciltno,
#                         nufus_sirano=e.nufus_sirano,
#                         meslek=e.meslek,
#                         kurum=e.kurum,
#                         is_unvani=e.is_unvani,
#                         # meterial=meterial.id,
#                         # education=e.egitimid
#
#                     )
#                     person.save()
#                     item.person = person
#                     item.save()
#                     sayi += 1
#
#
#             else:
#                 if Sporcular.objects.get(sporcuid=item.oldpk).kangrubu:
#                     sporcu = Sporcular.objects.get(sporcuid=item.oldpk).kangrubu
#                     if sporcu == "A(+)":
#                         item.person.bloodType = Person.A1
#                         item.save()
#                     elif sporcu == "AB(+)":
#                         item.person.bloodType = Person.AB1
#                         item.save()
#                     elif sporcu == "0(+)":
#                         item.person.bloodType = Person.O1
#                         item.save()
#                     elif sporcu == "B(+)":
#                         item.person.bloodType = Person.B1
#                         item.save()
#                     elif sporcu == "B(-)":
#                         item.person.bloodType = Person.B2
#                         item.save()
#                     elif sporcu == "0(-)":
#                         item.person.bloodType = Person.O2
#                         item.save()
#                     elif sporcu == "A(-)":
#                         item.person.bloodType = Person.A2
#                         item.save()
#                     elif sporcu == "AB(-)":
#                         item.person.bloodType = Person.AB2
#                         item.save()
#
#     print(sayi)
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def KangrubuHakem(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#     sayi = 0
#     test = Judge.objects.exclude(person__bloodType=None)
#     print(test.count())
#     athletes = Judge.objects.all()
#     print(athletes.count())
#     for item in athletes:
#
#         if Judge.objects.filter(oldpk=item.oldpk):
#             if item.person.tc != Sporcular.objects.get(sporcuid=item.oldpk).tcno:
#                 print(item)
#
#                 if Judge.objects.filter(oldpk=item.oldpk):
#                     e = Judge.objects.get(oldpk=item.oldpk)
#                     person = Person(
#                         tc=e.tcno,
#                         birthplace=e.dogumyeri,
#                         motherName=e.anneadi,
#                         fatherName=e.babaadi,
#                         birthDate=e.dogumtarihi,
#                         bloodType=e.kangrubu,
#                         # profileImage=e.resim,
#                         gender=e.cinsiyet,
#                         uyrukid=e.uyrukid,
#                         nufus_ailesirano=e.nufus_ailesirano,
#                         nufus_ciltno=e.nufus_ciltno,
#                         nufus_sirano=e.nufus_sirano,
#                         meslek=e.meslek,
#                         kurum=e.kurum,
#                         is_unvani=e.is_unvani,
#                         # meterial=meterial.id,
#                         # education=e.egitimid
#
#                     )
#                     person.save()
#                     item.person = person
#                     item.save()
#                     sayi += 1
#
#
#             else:
#                 if Sporcular.objects.get(sporcuid=item.oldpk).kangrubu:
#                     sporcu = Sporcular.objects.get(sporcuid=item.oldpk).kangrubu
#                     if sporcu == "A(+)":
#                         item.person.bloodType = Person.A1
#                         item.save()
#                     elif sporcu == "AB(+)":
#                         item.person.bloodType = Person.AB1
#                         item.save()
#                     elif sporcu == "0(+)":
#                         item.person.bloodType = Person.O1
#                         item.save()
#                     elif sporcu == "B(+)":
#                         item.person.bloodType = Person.B1
#                         item.save()
#                     elif sporcu == "B(-)":
#                         item.person.bloodType = Person.B2
#                         item.save()
#                     elif sporcu == "0(-)":
#                         item.person.bloodType = Person.O2
#                         item.save()
#                     elif sporcu == "A(-)":
#                         item.person.bloodType = Person.A2
#                         item.save()
#                     elif sporcu == "AB(-)":
#                         item.person.bloodType = Person.AB2
#                         item.save()
#
#     print(sayi)
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def Emanet(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#     sayi = 0
#     test = MalzHareket.objects.all()
#     print(test.count())
#     for item in test:
#         deposit = Deposit(
#             date=item.tarih,
#             count=item.miktar,
#
#         )
#         if item.aciklama:
#             deposit.description = item.aciklama
#         if item.malzemeid:
#             deposit.product = Products.objects.get(pk=item.malzemeid.malzemeid)
#         if item.kulupid:
#             deposit.club = SportsClub.objects.get(pk=item.kulupid.kulupid)
#         if item.aciklama:
#             deposit.description = item.aciklama
#         deposit.save()
#
#     print(sayi)
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def communicationAktar(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#     sayi = 0
#     test = Athlete.objects.filter(communication2=None)
#     print(test.count())
#     for item in test:
#         item.communication2 = item.communication
#         item.save()
#     test = Coach.objects.filter(communication2=None)
#     print(test.count())
#     for item in test:
#         item.communication2 = item.communication
#         item.save()
#     test = Judge.objects.filter(communication2=None)
#     print(test.count())
#     for item in test:
#         item.communication2 = item.communication
#         item.save()
#     test = DirectoryMember.objects.filter(communication2=None)
#     print(test.count())
#     for item in test:
#         item.communication2 = item.communication
#         item.save()
#     test = SportClubUser.objects.filter(communication2=None)
#     print(test.count())
#     for item in test:
#         item.communication2 = item.communication
#         item.save()
#
#     print(sayi)
#
#     return redirect('sbs:admin')
#
#
# @login_required
# def judgeAktar(request):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#
#     for item in Vizeler.objects.all():
#         print(item.sporcuid.sporcuid)
#         if Judge.objects.filter(oldpk=item.sporcuid.sporcuid):
#             judge = Judge.objects.get(oldpk=item.sporcuid.sporcuid)
#             grade = Level(
#                 definition=CategoryItem.objects.get(pk=7),
#                 expireDate=item.gecerliliktarihi,
#                 startDate=item.belgetarihi,
#                 branch=EnumFields.BADMİNTON.value
#             )
#             grade.levelType = EnumFields.LEVELTYPE.GRADE
#             grade.status = Level.APPROVED
#             grade.isActive = True
#             grade.save()
#             judge.grades.add(grade)
#             judge.save()
#
#             visa = Level(
#                 branch=EnumFields.BADMİNTON.value
#             )
#             visa.startDate = item.belgetarihi
#             visa.expireDate = item.gecerliliktarihi
#             visa.definition = CategoryItem.objects.get(forWhichClazz='VISA_REFEREE')
#             visa.levelType = EnumFields.LEVELTYPE.VISA
#             visa.status = Level.APPROVED
#
#             visa.isActive = True
#             visa.save()
#             judge.visa.add(visa)
#             judge.save()
#
#     return redirect('sbs:admin')
import time
import traceback

import pandas
import pandas as pd
import unidecode
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.shortcuts import redirect

from sbs.models import City, Communication, CategoryItem, HavaLevel, Branch, Coach, ActiveGroup
from sbs.models.tvfbf.SportFacility import SportFacility
from sbs.models.ekabis.Person import Person


def transmissionFacility(request):
    try:
        with transaction.atomic():

            df = pandas.read_csv('tesis.csv', encoding='utf8')
            x = ''
            for value in df.values.tolist():
                if value[1] and value[0]:

                    city_name = str(value[0]).encode('ascii', 'ignore').decode('ascii').upper()
                    if City.objects.filter(name=city_name):
                        disallowed_characters = './:,"'
                        for character in disallowed_characters:
                            name = str(value[1]).encode('ascii', 'ignore').decode('ascii').replace(character, "")
                            address = str(value[2]).encode('ascii', 'ignore').decode('ascii').replace(character, "")
                            phone = str(value[3]).encode('ascii', 'ignore').decode('ascii').replace(character, "")
                        if not SportFacility.objects.filter(name=name):
                            facility = SportFacility(name=name)
                            facility.save()
                            communation = Communication(phoneNumber=phone, city=city_name, address=address)
                            communation.save()
                            facility.communication = communation
                            facility.save()
            print('spor salonları eklendi')
            messages.success(request, 'Spor salonu kaydı tamamlandı')

            return redirect('sbs:view_admin')

    except Exception as e:
        messages.warning(request, e)
        traceback.print_exc()
        return redirect('sbs:view_admin')


def transmissionAntrenor(request):
    try:
        with transaction.atomic():

            df = pandas.read_csv(
                '/var/www/vhosts/sbs.tvgfbf.gov.tr/httpdocs/djangoProject/VucutGelistirmeFederasyonu/antrenor_list.csv')

            for value in df.values:
                if not User.objects.filter(username=value[1].lower()):
                    email = value[1].lower()
                    if not Person.objects.filter(user__first_name=value[3], user__last_name=value[4]).filter(
                            user__email=email):
                        city_name = None
                        branch = Branch.objects.get(title=value[2])

                        grade = CategoryItem.objects.get(name=value[0])
                        level = HavaLevel(branch=branch, definition=grade, city=city_name)
                        level.save()

                        user = User(username=email, email=email, first_name=value[3], last_name=value[4])
                        user.save()
                        group = Group.objects.get(name='Antrenör')
                        user.groups.add(group)
                        active = ActiveGroup(user=user, group=group)
                        active.save()

                        person = Person(user=user)
                        person.save()

                        phone = None
                        town = None
                        com = Communication(phoneNumber=phone, city=city_name, town=town)
                        com.save()

                        coach = Coach(person=person, communication=com)

                        coach.save()
                        coach.grades.add(level)
                        coach.branch.add(branch)
                        time.sleep(2)
            messages.success(request, 'Antrenör kaydı tamamlandı')

        print('antrenorler eklendi')
        return redirect('sbs:view_admin')

    except Exception as e:
        messages.warning(request, e)
        traceback.print_exc()
        return redirect('sbs:view_admin')


def transmissionAntrenorBelge(request, i, k):
    try:
        with transaction.atomic():
            coaches = Coach.objects.all()[i:k]
            for coach in coaches:
                if coach.grades.all():
                    if coach.grades.last().form:
                        name = coach.grades.last().form.name.encode('utf-8', errors='ignore')
                        name = name.decode('utf-8', errors='ignore')
                        coach.grades.last().form.name = name
                        coach.form = coach.grades.last().form
            messages.success(request, 'Antrenör belge transferi tamamlandı')

        print('antrenor belgeleri aktarıldı.')
        return redirect('sbs:view_admin')

    except Exception as e:
        messages.warning(request, e)
        traceback.print_exc()
        return redirect('sbs:view_admin')
