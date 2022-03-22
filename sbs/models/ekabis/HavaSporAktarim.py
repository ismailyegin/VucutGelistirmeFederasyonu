# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class SystemAdmin(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    logo = models.CharField(max_length=255)
    lastlogin = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'system_admin'


class SystemAutoLogin(models.Model):
    login_secret_id = models.CharField(max_length=64)
    user_secret_id = models.CharField(max_length=32)
    target = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'system_auto_login'


class SystemEbysAdminauth(models.Model):
    category = models.IntegerField()
    secret_id = models.CharField(max_length=9)
    title = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'system_ebys_adminauth'


class SystemEbysAthleteCoachAppend(models.Model):
    user_secret_id = models.CharField(max_length=32)
    club_flightscholl_secret_id = models.CharField(max_length=32)
    append_type = models.CharField(max_length=7)
    append_user_secret_id = models.CharField(max_length=32)
    append_date = models.DateField()
    suspended_user_secret_id = models.CharField(max_length=32)
    suspended_date = models.DateField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_athlete_coach_append'


class SystemEbysAuth(models.Model):
    user = models.IntegerField()
    auth = models.CharField(max_length=6)
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'system_ebys_auth'


class SystemEbysBranches(models.Model):
    secret_id = models.CharField(max_length=10)
    title = models.CharField(max_length=128)
    sort = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_branches'


class SystemEbysBranchesSub(models.Model):
    branch_secret_id = models.CharField(max_length=32)
    secret_id = models.CharField(max_length=32)
    title = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'system_ebys_branches_sub'


class SystemEbysCity(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'system_ebys_city'


class SystemEbysCoaches(models.Model):
    secret_id = models.CharField(max_length=32)
    tckimlik = models.CharField(max_length=11)
    namesurname = models.CharField(max_length=128)
    birthday = models.CharField(max_length=10)
    phone = models.CharField(max_length=14)
    email = models.CharField(max_length=128)
    address = models.TextField()
    city = models.IntegerField()
    iban = models.CharField(max_length=64)
    branches = models.TextField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_coaches'


class SystemEbysCommonuser(models.Model):
    secret_id = models.CharField(max_length=20)
    profilephoto = models.CharField(max_length=128)
    tckimlik = models.CharField(max_length=11)
    id_verify = models.IntegerField(db_column='ID_verify')  # Field name made lowercase.
    passportnumber = models.CharField(max_length=128)
    name = models.CharField(max_length=256)
    surname = models.CharField(max_length=128)
    birthday = models.DateField()
    bloodgroup = models.CharField(max_length=10)
    gender = models.CharField(max_length=5)
    phone = models.CharField(max_length=32)
    phone_verify = models.IntegerField()
    email = models.CharField(max_length=128)
    email_verify = models.IntegerField()
    password = models.CharField(max_length=128)
    address = models.TextField()
    city = models.IntegerField()
    iban = models.CharField(max_length=64)
    user_type = models.CharField(max_length=128)
    acildurum_kisi = models.CharField(max_length=64)
    acildurum_phone = models.CharField(max_length=32)
    heskodu = models.CharField(max_length=12)
    ip = models.CharField(max_length=32)
    useragent = models.TextField()
    ebys_admin_auth = models.TextField()
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'system_ebys_commonuser'


class SystemEbysCompetition(models.Model):
    secret_id = models.CharField(max_length=32)
    category_secret = models.CharField(max_length=32)
    title = models.CharField(max_length=256)
    city = models.IntegerField()
    start_date = models.CharField(max_length=10)
    finish_date = models.CharField(max_length=10)
    description = models.TextField()
    creator = models.CharField(max_length=32)
    created_date = models.DateTimeField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_competition'


class SystemEbysEbysmodule(models.Model):
    secret_id = models.CharField(max_length=32)
    title = models.CharField(max_length=64)
    icon = models.CharField(max_length=32)
    link = models.CharField(max_length=64)
    target = models.CharField(max_length=32)
    sort = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_ebysmodule'


class SystemEbysEducationseminar(models.Model):
    secret_id = models.CharField(max_length=32)
    city = models.CharField(max_length=16)
    branch = models.CharField(max_length=16)
    title = models.CharField(max_length=128)
    start_date = models.CharField(max_length=128)
    finish_date = models.CharField(max_length=128)
    edu_time = models.CharField(max_length=128)
    coaches = models.TextField()
    description = models.TextField()
    creator = models.CharField(max_length=32)
    created_date = models.DateTimeField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_educationseminar'


class SystemEbysEkipman(models.Model):
    secret_id = models.CharField(max_length=32)
    equipment_type = models.CharField(max_length=24)
    user_secret_id = models.CharField(max_length=32)
    club_secret_id = models.CharField(max_length=32)
    parasut_kanat_markasi = models.CharField(max_length=64)
    parasut_kanat_modeli = models.CharField(max_length=64)
    parasut_kanat_sinifi = models.CharField(max_length=64)
    parasut_kanat_renk = models.CharField(max_length=64)
    parasut_kanat_uretimyili = models.CharField(max_length=64)
    parasut_harnes_marka = models.CharField(max_length=64)
    parasut_harnes_model = models.CharField(max_length=64)
    parasut_harnes_renk = models.CharField(max_length=64)
    paramotor_marka = models.CharField(max_length=64)
    paramotor_model = models.CharField(max_length=64)
    paramotor_serino = models.CharField(max_length=64)
    paramotor_nereden_satinalindi = models.IntegerField()
    paramotor_firmakisi_bilgisi = models.CharField(max_length=64)
    paramotor_satinalma_tarih = models.CharField(max_length=32)
    drone_marka = models.CharField(max_length=128)
    drone_model = models.CharField(max_length=128)
    drone_renk = models.CharField(max_length=128)
    drone_agirlik = models.CharField(max_length=128)
    drone_serino = models.CharField(max_length=128)
    drone_plaka = models.CharField(max_length=128)
    date = models.DateField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_ekipman'


class SystemEbysEventApplication(models.Model):
    secret_id = models.CharField(max_length=128)
    user_secret_id = models.CharField(max_length=128)
    year = models.CharField(max_length=4)
    title = models.CharField(max_length=128)
    provience = models.CharField(max_length=64)
    start_date = models.DateField()
    finish_date = models.DateField()
    event_type = models.CharField(max_length=64)
    submit_date = models.DateTimeField()
    status_description = models.TextField()
    status_changed_secret_id = models.CharField(max_length=128)
    status_changed_date = models.DateTimeField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_event_application'


class SystemEbysEventJoin(models.Model):
    event_secret_id = models.CharField(max_length=32)
    user_secret_id = models.CharField(max_length=32)
    namesurname = models.CharField(max_length=256)
    progress = models.IntegerField()
    reserve_order = models.IntegerField()
    description = models.TextField()
    category = models.CharField(max_length=32)
    subcategory = models.CharField(max_length=256)
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'system_ebys_event_join'


class SystemEbysEventOfficer(models.Model):
    event_secret_id = models.CharField(max_length=32)
    user_secret_id = models.CharField(max_length=32)
    name_surname = models.CharField(max_length=64)
    referee_statu = models.CharField(max_length=64)
    task = models.CharField(max_length=64)
    added_secret_id = models.CharField(max_length=32)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_event_officer'


class SystemEbysFfsalonEtap(models.Model):
    event_secret_id = models.CharField(max_length=32)
    etap_1 = models.IntegerField()
    etap_2 = models.IntegerField()
    etap_3 = models.IntegerField()
    etap_4 = models.IntegerField()
    sontur = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_ffsalon_etap'


class SystemEbysGeneralFile(models.Model):
    secret_id = models.CharField(max_length=256)
    type = models.CharField(max_length=12)
    user_secret_id = models.CharField(max_length=128)
    title = models.CharField(max_length=256)
    description = models.TextField()
    file = models.CharField(max_length=256)
    created_secret_id = models.CharField(max_length=256)
    created_date = models.DateTimeField()
    updated_secret_id = models.CharField(max_length=256)
    updated_date = models.DateTimeField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_general_file'


class SystemEbysHedefEtap(models.Model):
    event_secret_id = models.CharField(max_length=32)
    etap_1 = models.IntegerField()
    etap_2 = models.IntegerField()
    etap_3 = models.IntegerField()
    etap_4 = models.IntegerField()
    etap_5 = models.IntegerField()
    etap_6 = models.IntegerField()
    sontur = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_hedef_etap'


class SystemEbysHedefSampiyona(models.Model):
    year = models.CharField(max_length=32)
    user_secret_id = models.CharField(max_length=32)
    namesurname = models.CharField(max_length=64)
    cinsiyet = models.CharField(max_length=5)
    puan = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_hedef_sampiyona'


class SystemEbysHedefSampiyonaKulup(models.Model):
    year = models.CharField(max_length=32)
    club_secret_id = models.CharField(max_length=32)
    kulup = models.CharField(max_length=64)
    puan = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_hedef_sampiyona_kulup'


class SystemEbysImacEtap(models.Model):
    event_secret_id = models.CharField(max_length=32)
    etap_1 = models.IntegerField()
    etap_2 = models.IntegerField()
    etap_3 = models.IntegerField()
    etap_4 = models.IntegerField()
    sontur = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_imac_etap'


class SystemEbysKura(models.Model):
    secret_id = models.CharField(max_length=64)
    event_secret_id = models.CharField(max_length=64)
    user_secret_id = models.CharField(max_length=64)
    cekilen_kura = models.TextField()
    kura_status = models.IntegerField()
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'system_ebys_kura'


class SystemEbysKuraSonuclari(models.Model):
    event_secret_id = models.CharField(max_length=64)
    sportsman_secret_id = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    sort = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_kura_sonuclari'


class SystemEbysLoginPc(models.Model):
    user_secret_id = models.CharField(max_length=256)
    login_date = models.DateTimeField()
    login_secret_id = models.CharField(max_length=256)
    ip = models.CharField(max_length=256)
    ua = models.TextField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_login_pc'


class SystemEbysLoginauth(models.Model):
    secret_id = models.CharField(max_length=32)
    sms_auth = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'system_ebys_loginauth'


class SystemEbysMemberLog(models.Model):
    secret_id = models.CharField(max_length=32)
    user_secret_id = models.CharField(max_length=64)
    more_user_secret_id = models.TextField()
    transaction = models.TextField()
    batch_transaction = models.CharField(max_length=22)
    server_ip = models.CharField(max_length=64)
    server_ua = models.TextField()
    server_as = models.CharField(max_length=256)
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'system_ebys_member_log'


class SystemEbysMembershipAthlete(models.Model):
    user_secret_id = models.CharField(max_length=128)
    branch = models.TextField()
    airtribune_id = models.CharField(max_length=128)
    sporculisansno = models.CharField(max_length=128)
    lisansgecerlilik = models.DateField()
    lisansfoto = models.CharField(max_length=128)
    kulup = models.CharField(max_length=128)
    sigortasirketi = models.CharField(max_length=128)
    sigortapolice = models.CharField(max_length=128)
    egitimyer = models.CharField(max_length=256)
    ucusatlayis = models.CharField(max_length=256)
    basarilariniz = models.CharField(max_length=256)
    son12ay = models.CharField(max_length=256)
    toplamsorti = models.CharField(max_length=256)
    sertifikaderece = models.CharField(max_length=256)
    lisanslar = models.CharField(max_length=256)
    boy = models.CharField(max_length=256)
    kilo = models.CharField(max_length=256)
    infolevel = models.IntegerField()
    infostatus = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_membership_athlete'


class SystemEbysMembershipClub(models.Model):
    user_secret_id = models.CharField(max_length=128)
    branch = models.CharField(max_length=256)
    kulupadi = models.CharField(max_length=256)
    kulupyetkili = models.CharField(max_length=128)
    kuluptelefon = models.CharField(max_length=128)
    kulupeposta = models.CharField(max_length=256)
    kulupadres = models.CharField(max_length=128)
    kulupil = models.IntegerField()
    infolevel = models.IntegerField()
    infostatus = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_membership_club'


class SystemEbysMembershipCoach(models.Model):
    user_secret_id = models.CharField(max_length=128)
    branch = models.CharField(max_length=256)
    nufuscuzdani = models.CharField(max_length=128)
    diploma = models.CharField(max_length=128)
    sabikakaydi = models.CharField(max_length=128)
    cezayazisi = models.CharField(max_length=128)
    saglikbeyanformu = models.CharField(max_length=128)
    antrenorbelgesi = models.CharField(max_length=128)
    infolevel = models.IntegerField()
    infostatus = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_membership_coach'


class SystemEbysMembershipFlightscholl(models.Model):
    user_secret_id = models.CharField(max_length=128)
    branch = models.CharField(max_length=256)
    kulupadi = models.CharField(max_length=256)
    kulupyetkili = models.CharField(max_length=128)
    kuluptelefon = models.CharField(max_length=128)
    kulupeposta = models.CharField(max_length=256)
    kulupadres = models.CharField(max_length=128)
    kulupil = models.IntegerField()
    infolevel = models.IntegerField()
    infostatus = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_membership_flightscholl'


class SystemEbysMembershipOrganizer(models.Model):
    user_secret_id = models.CharField(max_length=128)
    branch = models.CharField(max_length=256)
    firmaunvani = models.CharField(max_length=256)
    firmayetkilisi = models.CharField(max_length=128)
    firmavdaire = models.CharField(max_length=128)
    firmavno = models.CharField(max_length=128)
    firmatelefon = models.CharField(max_length=128)
    firmaeposta = models.CharField(max_length=128)
    firmaadres = models.CharField(max_length=256)
    infolevel = models.IntegerField()
    infostatus = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_membership_organizer'


class SystemEbysMembershipReferee(models.Model):
    user_secret_id = models.CharField(max_length=128)
    branch = models.CharField(max_length=256)
    nufuscuzdani = models.CharField(max_length=128)
    diploma = models.CharField(max_length=128)
    sabikakaydi = models.CharField(max_length=128)
    cezayazisi = models.CharField(max_length=128)
    saglikbeyanformu = models.CharField(max_length=128)
    hakembilgiformu = models.CharField(max_length=128)
    infolevel = models.IntegerField()
    infostatus = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_membership_referee'


class SystemEbysMesafeScore(models.Model):
    event_secret_id = models.CharField(max_length=128)
    event_day_date = models.DateField()
    day_type = models.IntegerField()
    task_overall = models.CharField(max_length=256)
    task_sports = models.CharField(max_length=256)
    task_women = models.CharField(max_length=256)
    task_clubs = models.CharField(max_length=256)
    task_turkishnat = models.CharField(max_length=256)
    comp_overall = models.CharField(max_length=256)
    comp_sports = models.CharField(max_length=256)
    comp_women = models.CharField(max_length=256)
    comp_clubs = models.CharField(max_length=256)
    comp_turkishnat = models.CharField(max_length=256)
    full_icg = models.CharField(max_length=256)
    task_status = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'system_ebys_mesafe_score'


class SystemEbysMilliSporcu(models.Model):
    user_secret_id = models.CharField(max_length=32)
    branch_secret_id = models.CharField(max_length=32)
    branch_sub_cat = models.CharField(max_length=32)
    belge_yili = models.IntegerField()
    belge_no = models.CharField(max_length=32)
    belge_sinifi = models.CharField(max_length=32)
    belge_dogrulama_kodu = models.CharField(max_length=32)
    milli_oldugu_organizasyon = models.CharField(max_length=128)
    moo_baslangic_bitis = models.CharField(max_length=32)
    moo_ulke_sayisi = models.CharField(max_length=64)
    moo_sporcu_sayisi = models.CharField(max_length=64)
    millilik_belgesi = models.CharField(max_length=64)
    created_date = models.DateTimeField()
    created_user = models.CharField(max_length=32)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_milli_sporcu'


class SystemEbysPasswordauth(models.Model):
    secret_id = models.CharField(max_length=255)
    user_secret_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'system_ebys_passwordauth'


class SystemEbysPersonal(models.Model):
    secret_id = models.CharField(max_length=16)
    category_secret = models.CharField(max_length=16)
    tckimlik = models.CharField(max_length=16)
    namesurname = models.CharField(max_length=64)
    subtitle = models.CharField(max_length=128)
    birthday = models.CharField(max_length=10)
    gender = models.CharField(max_length=5)
    phone = models.CharField(max_length=14)
    email = models.CharField(max_length=128)
    nufus_il = models.IntegerField()
    nufus_ilce = models.CharField(max_length=128)
    home_address = models.TextField()
    emergency_title = models.CharField(max_length=128)
    emergency_number = models.CharField(max_length=14)
    bloodgroup = models.CharField(max_length=20)
    hastaliklar = models.CharField(max_length=256)
    alerji = models.CharField(max_length=256)
    ise_baslama_tarihi = models.CharField(max_length=10)
    iban = models.CharField(max_length=64)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_personal'


class SystemEbysPersonalCategory(models.Model):
    secret_id = models.CharField(max_length=16)
    title = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'system_ebys_personal_category'


class SystemEbysPuanDurumuFfsalon(models.Model):
    event_secret_id = models.CharField(max_length=32)
    user_secret_id = models.CharField(max_length=32)
    puan_1 = models.CharField(max_length=11)
    puan_1_status = models.IntegerField()
    puan_2 = models.CharField(max_length=11)
    puan_2_status = models.IntegerField()
    puan_3 = models.CharField(max_length=11)
    puan_3_status = models.IntegerField()
    puan_4 = models.CharField(max_length=11)
    puan_4_status = models.IntegerField()
    toplam_puan = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_puan_durumu_ffsalon'


class SystemEbysPuanDurumuHedef(models.Model):
    event_secret_id = models.CharField(max_length=32)
    user_secret_id = models.CharField(max_length=32)
    puan_1 = models.IntegerField()
    puan_1_status = models.IntegerField()
    puan_2 = models.IntegerField()
    puan_2_status = models.IntegerField()
    puan_3 = models.IntegerField()
    puan_3_status = models.IntegerField()
    puan_4 = models.IntegerField()
    puan_4_status = models.IntegerField()
    puan_5 = models.IntegerField()
    puan_5_status = models.IntegerField()
    puan_6 = models.IntegerField()
    puan_6_status = models.IntegerField()
    toplam_puan = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_puan_durumu_hedef'


class SystemEbysPuanDurumuImac(models.Model):
    event_secret_id = models.CharField(max_length=32)
    user_secret_id = models.CharField(max_length=32)
    puan_1 = models.CharField(max_length=11)
    puan_1_status = models.IntegerField()
    puan_2 = models.CharField(max_length=11)
    puan_2_status = models.IntegerField()
    puan_3 = models.CharField(max_length=11)
    puan_3_status = models.IntegerField()
    puan_4 = models.CharField(max_length=11)
    puan_4_status = models.IntegerField()
    toplam_puan = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'system_ebys_puan_durumu_imac'


class SystemEbysRefereeStatu(models.Model):
    user_secret_id = models.CharField(max_length=64)
    branch_secret_id = models.CharField(max_length=64)
    statu = models.CharField(max_length=18)
    statu_change_date = models.DateField()
    statu_change_user = models.CharField(max_length=32)
    statu_changer_db_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'system_ebys_referee_statu'


class SystemEbysSmsemailAuth(models.Model):
    user = models.CharField(max_length=32)
    type = models.CharField(max_length=5)
    auth_code = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'system_ebys_smsemail_auth'


class SystemEbysSmslist(models.Model):
    secret_id = models.CharField(max_length=32)
    record_secret_id = models.CharField(max_length=32)
    namesurname = models.CharField(max_length=64)
    phone = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'system_ebys_smslist'


class SystemEbysSmslistCategory(models.Model):
    secret_id = models.CharField(max_length=32)
    title = models.CharField(max_length=128)
    creator = models.CharField(max_length=32)
    created_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'system_ebys_smslist_category'


class SystemEbysSmssendLog(models.Model):
    secret_id = models.CharField(max_length=32)
    smslist_category = models.CharField(max_length=32)
    sms_number = models.CharField(max_length=32)
    message = models.TextField()
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'system_ebys_smssend_log'


class SystemEbysTezcan(models.Model):
    adi = models.CharField(max_length=255)
    soyadi = models.CharField(max_length=255)
    dogumyeri = models.CharField(max_length=255)
    dogumtarihi = models.CharField(max_length=255)
    tckimik = models.CharField(max_length=255)
    eposta = models.CharField(max_length=255)
    ulke = models.CharField(max_length=255)
    sehir = models.CharField(max_length=255)
    ikametadres = models.TextField()
    ceptelefonu = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'system_ebys_tezcan'


class SystemEbysTezcanArakayit(models.Model):
    secret_id = models.CharField(max_length=32)
    ad = models.CharField(max_length=64)
    soyad = models.CharField(max_length=64)
    tckimlik = models.CharField(max_length=11)
    dtarih = models.DateField()
    eposta = models.CharField(max_length=128)
    phone = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'system_ebys_tezcan_arakayit'


class SystemEbysTezcanRecord(models.Model):
    adsoyad = models.CharField(max_length=64)
    tckimlik = models.CharField(max_length=11)
    dtarih = models.CharField(max_length=10)
    telefon = models.CharField(max_length=14)
    eposta = models.CharField(max_length=64)
    username = models.CharField(max_length=64)
    photo = models.CharField(max_length=64)
    kulup = models.CharField(max_length=64)
    odul = models.CharField(max_length=64)
    video = models.CharField(max_length=256)
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'system_ebys_tezcan_record'


class SystemEbysUser(models.Model):
    secret_id = models.CharField(max_length=32)
    profilpicture = models.CharField(max_length=128)
    namesurname = models.CharField(max_length=64)
    phone = models.CharField(max_length=32)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    permission = models.TextField()
    login_sms = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_ebys_user'


class SystemGeciciKulubSporcu(models.Model):
    event_secret_id = models.CharField(max_length=32)
    club_secret_id = models.CharField(max_length=32)
    kulup = models.CharField(max_length=128)
    sporcular = models.TextField()
    toplampuan = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_gecici_kulub_sporcu'


class SystemLoginredirect(models.Model):
    redirect = models.CharField(max_length=32)
    user_secret_id = models.CharField(max_length=64)
    login_secret_id = models.CharField(max_length=64)
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'system_loginredirect'


class SystemModulemap(models.Model):
    modulename = models.CharField(db_column='moduleName', max_length=255)  # Field name made lowercase.
    moduleicon = models.CharField(db_column='moduleIcon', max_length=255)  # Field name made lowercase.
    moduletablename = models.CharField(db_column='moduleTableName', max_length=255)  # Field name made lowercase.
    moduleurl = models.CharField(db_column='moduleUrl', max_length=255)  # Field name made lowercase.
    modulelang = models.TextField(db_column='moduleLang')  # Field name made lowercase.
    modulelangurl = models.CharField(db_column='moduleLangUrl', max_length=256)  # Field name made lowercase.
    modulelangalign = models.CharField(db_column='moduleLangAlign', max_length=256)  # Field name made lowercase.
    moduletype = models.IntegerField(db_column='moduleType')  # Field name made lowercase.
    relatedmodule = models.CharField(db_column='relatedModule', max_length=255)  # Field name made lowercase.
    modulesort = models.IntegerField(db_column='moduleSort')  # Field name made lowercase.
    modulemediapath = models.CharField(db_column='moduleMediaPath', max_length=64)  # Field name made lowercase.
    modulemediaresize = models.IntegerField(db_column='moduleMediaResize')  # Field name made lowercase.
    resizebigwidth = models.IntegerField(db_column='resizeBigWidth')  # Field name made lowercase.
    resizebigheight = models.IntegerField(db_column='resizeBigHeight')  # Field name made lowercase.
    resizesmallwidth = models.IntegerField(db_column='resizeSmallWidth')  # Field name made lowercase.
    resizesmallheight = models.IntegerField(db_column='resizeSmallHeight')  # Field name made lowercase.
    dbjson = models.TextField()

    class Meta:
        managed = False
        db_table = 'system_modulemap'


class SystemUtsAdmin(models.Model):
    title = models.CharField(max_length=256)
    email = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'system_uts_admin'


class SystemUtsCity(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'system_uts_city'


class SystemUtsClub(models.Model):
    title = models.CharField(max_length=256)
    authorized = models.CharField(max_length=256)
    antrenor = models.CharField(max_length=256)
    phone = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    address = models.TextField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_uts_club'


class SystemUtsEquipment(models.Model):
    type = models.IntegerField()
    pilot_id = models.IntegerField()
    club_id = models.IntegerField()
    kanat_markasi = models.CharField(max_length=64)
    kanat_sinifi = models.CharField(max_length=64)
    kanat_rengi = models.CharField(max_length=64)
    harnes = models.CharField(max_length=256)
    paramotor_markasi = models.CharField(max_length=64)
    paramotor_serino = models.CharField(max_length=64)
    nereden_satinalindi = models.IntegerField()
    firma_kisi_bilgisi = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'system_uts_equipment'


class SystemUtsEvent(models.Model):
    secret_id = models.CharField(max_length=32)
    created = models.CharField(max_length=32)
    type = models.IntegerField()
    type_2 = models.IntegerField()
    takeoff = models.IntegerField()
    title = models.CharField(max_length=256)
    date = models.DateField()
    time = models.CharField(max_length=64)
    cities = models.CharField(max_length=128)
    pilot_list = models.TextField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_uts_event'


class SystemUtsJandarma(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    eposta = models.CharField(max_length=256)
    telefon = models.CharField(max_length=256)
    faks = models.CharField(max_length=256)
    adres = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'system_uts_jandarma'


class SystemUtsPilot(models.Model):
    name = models.CharField(max_length=256)
    surname = models.CharField(max_length=256)
    tckimlik = models.CharField(max_length=11)
    phone = models.CharField(max_length=14)
    email = models.CharField(max_length=256)
    birthday = models.DateField()

    class Meta:
        managed = False
        db_table = 'system_uts_pilot'


class SystemUtsPreregistration(models.Model):
    tckimlik = models.IntegerField()
    ad = models.CharField(max_length=256)
    soyad = models.CharField(max_length=256)
    dtarih = models.DateField()
    eposta = models.CharField(max_length=256)
    telefon = models.CharField(max_length=14)

    class Meta:
        managed = False
        db_table = 'system_uts_preregistration'


class SystemUtsSignupauth(models.Model):
    record_id = models.IntegerField()
    user_type = models.IntegerField()
    email_auth = models.IntegerField()
    email_confirm = models.IntegerField()
    phone_auth = models.IntegerField()
    phone_confirm = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_uts_signupauth'


class SystemUtsTakeoff(models.Model):
    city = models.IntegerField()
    coor_lat = models.CharField(max_length=256)
    coor_long = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    adres = models.TextField()
    ucus_saati = models.CharField(max_length=256)
    kalkis_alani_koordinat = models.CharField(max_length=256)
    kalkis_alani_yukseklik = models.CharField(max_length=256)
    inis_alani_koordinat = models.CharField(max_length=256)
    inis_alani_yukseklik = models.CharField(max_length=256)
    ucus_yapilacak_yaricap = models.CharField(max_length=256)
    maksimum_irtifa = models.CharField(max_length=256)
    kalkis_yonleri = models.TextField()
    pilot_seviyesi = models.TextField()
    yol_durumu = models.TextField()
    aciklamalar = models.TextField()

    class Meta:
        managed = False
        db_table = 'system_uts_takeoff'


class SystemUtsUser(models.Model):
    record_id = models.IntegerField()
    type_id = models.IntegerField()
    email = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'system_uts_user'


class TempRegistrationData(models.Model):
    reg_id = models.PositiveIntegerField()
    reg_time = models.IntegerField()
    user_name = models.CharField(max_length=12)
    user_pass = models.TextField()
    user_salt = models.CharField(max_length=32)
    user_email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    street_address = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'temp_registration_data'


