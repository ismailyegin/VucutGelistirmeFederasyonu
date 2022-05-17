from django.urls import path

from sbs.Views import ClubViews, RefereeViews, CoachViews, TransmissionViews, \
    ClubTransmissionViews, DocumentViews, SportFacilityViews, AnnouncementViews, Aktarma
from sbs.Views.ekabis import APIViews, AdminViews, \
    LogViews, CityViews, UserViews, \
    HelpViews, PermissionView, GroupView, \
    HelpMenuViews, NotificationViews, DirectoryViews
from sbs.Views import DashboardViews
app_name = 'sbs'

urlpatterns = [
    # Dashboard
    path('anasayfa/admin/', DashboardViews.return_admin_dashboard, name='view_admin'),
    path('anasayfa/sehir-sporcu-sayisi', DashboardViews.City_athlete_cout, name='sehir-sporcu-sayisi'),
    path('anasayfa/hakem', DashboardViews.return_referee_dashboard, name='hakem'),
    path('anasayfa/antrenor', DashboardViews.return_coach_dashboard, name='antrenor'),
    path('anasayfa/federasyon', DashboardViews.return_directory_dashboard, name='federasyon'),
    path('anasayfa/kulup-uyesi', DashboardViews.return_club_user_dashboard, name='kulup-uyesi'),

    # ANTRENÖR

    path('antrenorler/', CoachViews.return_coachs, name='return_coachs'),
    path('antrenor-ekle/', CoachViews.return_add_coach, name='add_coach'),
    path('antrenor-duzenle/<uuid:uuid>', CoachViews.coachUpdate, name='update_coach'),
    path('antrenor/antrenorler/sil/', CoachViews.delete_coach, name='delete-coach'),
    path('antrenor/antrenor-kademe-ekle/<uuid:uuid>', CoachViews.add_coach_referee, name='add_grade_coach'),
    path('antrenor/antrenor-kademe-onayla/<uuid:grade_uuid>/<uuid:coach_uuid>', CoachViews.grade_approval,
         name='coach_grade_approval'),
    path('antrenor/antrenor-kademe-reddet/<uuid:grade_uuid>/<uuid:coach_uuid>', CoachViews.grade_reject,
         name='coach_grade_reject'),
    path('antrenor/antrenor-kademe-guncelle/<uuid:grade_uuid>/<uuid:coach_uuid>', CoachViews.update_grade,
         name='coach_update_grade'),
    path('antrenor/antrenor-kademe-sil/', CoachViews.delete_grade, name='coach_delete_grade'),
    path('antrenor/antrenor-vize-ekle/<uuid:uuid>', CoachViews.add_visa_coach, name='add_visa_coach'),
    path('antrenor/antrenor-vize-onayla/<uuid:visa_uuid>/<uuid:coach_uuid>', CoachViews.visa_approval,
         name='coach_visa_approval'),
    path('antrenor/antrenor-vize-reddet/<uuid:visa_uuid>/<uuid:coach_uuid>', CoachViews.visa_reject,
         name='coach_visa_reject'),
    path('antrenor/antrenor-vize-guncelle/<uuid:visa_uuid>/<uuid:coach_uuid>', CoachViews.visa_update,
         name='coach_update_visa'),
    path('antrenor/antrenor-vize-duzenle/sil/', CoachViews.visa_delete, name='coach_delete_visa'),

    path('antrenor/kademe/', CoachViews.return_grade, name='return_grade'),
    path('antrenor/kademe/guncelle/<uuid:uuid>', CoachViews.gradeUpdate, name='update_grades'),
    path('antrenor/kademe/sil/', CoachViews.gradeDelete, name='delete_grades'),
    path('antrenor/kademe-listesi/', CoachViews.gradeList, name='coach_grade_list'),
    path('antrenor/kademe-listesi/onayla/<uuid:uuid>', CoachViews.gradeListApproval,
         name='coach_grade_list_approval'),
    path('antrenor/kademe-listesi/reddet/<uuid:uuid>', CoachViews.gradeListReject, name='coach_grade_list_reject'),
    path('antrenor/kademe-listesi-onayla-hepsi', CoachViews.gradeListApprovalAll,
         name='coach_grade-list-approval-all'),
    path('antrenor/kademe-listesi-reddet-hepsi', CoachViews.gradeListRejectAll,
         name='coach_grade-list-reject-all'),
    path('antrenor/vize-listesi/', CoachViews.visaList, name='coach_visa_list'),
    path('antrenor/vize-listesi/onayla/<uuid:uuid>', CoachViews.visaListApproval,
         name='coach_visa_list_approval'),
    path('antrenor/vize-listesi/reddet/<uuid:uuid>', CoachViews.visaListReject, name='coach_visa_list_reject'),

    # HAKEM
    path('hakemler/', RefereeViews.return_referees, name='return_referees'),
    path('hakem-ekle/', RefereeViews.return_add_referee, name='add_referee'),
    path('hakem-duzenle/<uuid:uuid>', RefereeViews.update_referee, name='update_referee'),
    path('hakem/hakemler/sil/', RefereeViews.delete_referee, name='delete-referee'),
    path('hakem/hakem-kademe-ekle/<uuid:uuid>', RefereeViews.add_grade_referee, name='add_grade_referee'),
    path('hakem/hakem-kademe-onayla/<uuid:grade_uuid>/<uuid:referee_uuid>', RefereeViews.grade_approval,
         name='grade_approval'),
    path('hakem/hakem-kademe-/reddet/<uuid:grade_uuid>/<uuid:referee_uuid>', RefereeViews.grade_reject,
         name='grade_reject'),
    path('hakem/hakem-kademe-duzenle/<uuid:grade_uuid>/<uuid:referee_uuid>', RefereeViews.update_grade,
         name='update_grade'),
    path('hakem/hakem-kademe-duzenle/sil/', RefereeViews.delete_grade, name='delete_grade'),
    path('hakem/hakem-vize-ekle/<uuid:uuid>', RefereeViews.add_visa_referee, name='add_visa_referee'),
    path('hakem/hakem-vize-onayla/<uuid:visa_uuid>/<uuid:referee_uuid>', RefereeViews.visa_approval,
         name='visa_approval'),
    path('hakem/hakem-vize-reddet/<uuid:visa_uuid>/<uuid:referee_uuid>', RefereeViews.visa_reject,
         name='visa_reject'),
    path('hakem/hakem-vize-guncelle/<uuid:visa_uuid>/<uuid:referee_uuid>', RefereeViews.visa_update,
         name='update_visa'),
    path('hakem/hakem-vize-duzenle/sil/', RefereeViews.visa_delete, name='delete_visa'),

    path('hakem/seviye/', RefereeViews.return_level, name='return_levels'),
    path('hakem/seviye/guncelle/<uuid:uuid>', RefereeViews.levelUpdate, name='update_level'),
    path('hakem/seviye/sil/', RefereeViews.levelDelete, name='delete_level'),
    path('hakem/kademe-listesi/', RefereeViews.gradeList, name='grade_list'),
    path('hakem/kademe-listesi/onayla/<uuid:uuid>', RefereeViews.gradeListApproval,
         name='grade_list_approval'),
    path('hakem/kademe-listesi/reddet/<uuid:uuid>', RefereeViews.gradeListReject, name='grade_list_reject'),
    path('hakem/kademe-listesi-onayla-hepsi', RefereeViews.gradeListApprovalAll,
         name='grade-list-approval-all'),
    path('hakem/kademe-listesi-reddet-hepsi', RefereeViews.gradeListRejectAll,
         name='grade-list-reject-all'),
    path('hakem/vize-listesi/', RefereeViews.visaList, name='visa_list'),
    path('hakem/vize-listesi/onayla/<uuid:uuid>', RefereeViews.visaListApproval,
         name='visa_list_approval'),
    path('hakem/vize-listesi/reddet/<uuid:uuid>', RefereeViews.visaListReject, name='visa_list_reject'),

    # KULUP
    path('kulupler', ClubViews.return_clubs,
         name='return_clubs'),
    path('kulup-ekle', ClubViews.add_club, name='add_club'),
    path(r'kulup-duzenle/<uuid:uuid>', ClubViews.clubUpdate,
         name='update_club'),
    path('kulup/kulup-ekle-api/', TransmissionViews.transmissionOffsetLimit, name='kulup-ekle-api'),
    path('kulup/kulup-getir-api/', TransmissionViews.GetCurrentClubDetail, name='kulup-getir-api'),

    path('kulup/kulup-sil/', ClubViews.club_delete, name='club-delete'),
    path('kulup/kulup-uye-sil/', ClubViews.deleteClubUserFromClub, name='deleteClubUserFromClub'),
    path('kulup/kulup-antrenor-sil/', ClubViews.deleteCoachFromClub, name='deleteCoachFromClub'),
    path('antrenor/antrenor-detay-api/', CoachViews.detailCoach, name='detailCoach-api'),
    path('antrenor/kulup-yetkili-detay-api/', ClubViews.detailClubUser, name='detailClubUser-api'),
    path('kulup/kulup-uyesi-ekle/<uuid:uuid>', ClubViews.return_add_club_person, name='kulup-uyesi-ekle'),
    path('kulup/antrenorSec/<uuid:uuid>', ClubViews.choose_coach_clup,
         name='choose-coach-club'),
    path('kulup/basvuru-listesi', ClubViews.return_preRegistration, name='ReferenceClubList'),
    path('kulup/basvuru/onayla/<int:pk>', ClubViews.approve_preRegistration, name='approveClub'),
    path('kulup/basvuru/reddet/<int:pk>', ClubViews.rejected_preRegistrationClub, name='rejectedClub'),
    path('kulup/basvuru/duzenle/<int:pk>', ClubViews.updateReferenceClub, name='updateReferenceClub'),

    path('kulupAktarimi/', ClubTransmissionViews.ClubTransmission, name='api-club-transmission'),
    path('kulup/kulup-yonetici-ekle-api/', TransmissionViews.getClubForRegisterManager,
         name='kulup-yönetici-ekle-api'),
    path('kulupAktarimi/limit-offset/', TransmissionViews.getLimitOffset, name='getLimitOffset'),
    path('il/il-aktarimi/', TransmissionViews.TransmissionCity, name='TransmissionCity'),
    path('ulke/ulke-aktarimi/', TransmissionViews.TransmissionCountry, name='TransmissionCountry'),
    path('ilce/ilce-aktarimi/', TransmissionViews.TransmissionDistrict, name='TransmissionDistrict'),

    # Yönetim
    path('kurul/kurul-uyeleri/', DirectoryViews.return_directory_members, name='view_directoryMember'),
    path('kurul/kurul-uyesi-ekle/', DirectoryViews.add_directory_member, name='add_directorymember'),
    path('kurul/kurul-uyesi-duzenle/<uuid:uuid>/', DirectoryViews.update_directory_member,
         name='change_directorymember'),
    path('kurul/kurul-uyeleri/sil/', DirectoryViews.delete_directory_member, name='delete_directorymember'),

    # yönetim rol
    path('kurul/kurul-uye-rolleri/', DirectoryViews.return_member_roles, name='view_directorymemberrole'),
    path('kurul/kurul-uye-rolleri/sil/', DirectoryViews.delete_member_role,
         name='delete_directorymemberrole'),
    path('kurul/kurul-uye-rol-duzenle/<uuid:uuid>/', DirectoryViews.update_member_role,
         name='change_directorymemberrole'),
    # yönetim kurul

    path('kurul/kurul-listesi', DirectoryViews.return_commissions, name='view_directorycommission'),
    path('kurul/kurul-sil/', DirectoryViews.delete_commission, name='delete_directorycommission'),
    path('kurul/kurul-duzenle/<uuid:pk>/', DirectoryViews.update_commission, name='change_directorycommission'),

    # Kullanıcılar
    path('kullanici/kullanicilar/', UserViews.return_users, name='view_user'),
    path('kullanici/kullanici-duzenle/<int:pk>/', UserViews.update_user, name='change_user'),
    path('kullanici/kullanicilar/aktifet<int:pk>/', UserViews.active_user, name='view_status'),
    path('kullanici/kullanici-mail-gonder/<int:pk>/', UserViews.send_information, name='view_email'),
    path('kullanici/kullanici-group-guncelle/<int:pk>/', UserViews.change_group_function, name='change_user_group'),

    # profil güncelle
    # path('admin/admin-profil-guncelle/', AdminViews.updateProfile,
    #      name='admin-profil-guncelle'),
    #
    # path('yonetim/yonetim-kurul-profil-guncelle/', DirectoryViews.updateDirectoryProfile,
    #      name='yonetim-kurul-profil-guncelle'),

    #   log kayıtlari
    path('log/log-kayitlari/', LogViews.view_log, name='view_logs'),

    # activ grup  güncelle
    path('rol/guncelle/<int:pk>/', DashboardViews.activeGroup, name='change_activegroup'),

    # guruplar arasında tasıma işlemi
    path('rol/degisitir/<int:pk>/', AdminViews.activeGroup, name='sporcu-aktive-group'),

    #     Yardım
    path('destek/yardim', HelpViews.help, name='view_help'),

    # Grup
    path('grup/grup-ekle/', GroupView.add_group, name='add_group'),
    path('grup/grup-listesi/', GroupView.return_list_group, name='view_group'),
    path('grup/grup-guncelleme/<int:pk>/', GroupView.return_update_group, name='change_group'),
    # grup izinleri
    path('grup/grup-izin-ekle/<int:pk>', GroupView.change_groupPermission, name='change_groupPermission'),
    # Ayarlar

    # Yeka
    path('ilce/ilce-getir/', CityViews.get_districts, name='ilce-getir'),

    # Yardım Menusu
    path('yardim/yardim-metni-ekle/', HelpMenuViews.help_text_add, name='add_help_text'),
    path('yardim/yardim-metin-listesi/', HelpMenuViews.return_help_text, name='view_help_text'),
    path('yardim/yardim-metni-duzenle/<uuid:uuid>', HelpMenuViews.update_help_menu, name='change_help_text'),

    path('log/api-log-listesi/', APIViews.GetLog.as_view(), name='view_log_api'),

    # Mahalle
    path('mahalle/mahalle-getir/', CityViews.get_neighborhood, name='get_neighborhood'),

    path('izin/izin-listesi/', PermissionView.view_permission, name='view_permission'),
    path('izin/izin-guncelle/<uuid:uuid>', PermissionView.change_permission, name='change_permission'),

    path('bildirim/bildirim-getir/', NotificationViews.get_notification, name='bildirim-getir'),
    path('bildirim/bildirimler/', NotificationViews.view_notification, name='bildirimler'),
    path('bildirim/bildirim-okundu/<int:id>', NotificationViews.is_read, name='bildirim-okundu-yap'),
    path('bildirim/okundu-isaretle/', NotificationViews.make_is_read, name='bildirim-okundu-isaretle'),

    # path('yeka/il/', CityViews.add_city, name='city_add'),
    # path('yeka/ilce/', CityViews.add_district, name='´district_add'),
    # path('yeka/mahalle/', CityViews.add_neighborhood, name='neighborhood_add'),
    # path('yeka/is-bloklari/', BusinessBlogViews.data_business_blog, name='business_block_add'),
    # path('yeka/is-blok-parametre/', BusinessBlogViews.data_parameter, name='data_business_block_parameter'),
    # path('yeka/is-blok-parametre-id/', BusinessBlogViews.data_parameter_block_id, name='data_block_parameter_id'),
    path('bildirim/tum-bildirim-okundu-yap/', NotificationViews.read_notification_all, name='read_notification_all'),

    # Bütçe

    # --------------------------------- HAVA SPORLARI -----------------------------------------------------------------

    # HAKEM VİZE SEMİNER

    path('hakem/visa-seminar', RefereeViews.returnVisaSeminar, name='referee-visa-seminar'),
    path('hakem/visa-seminar-ekle', RefereeViews.addVisaSeminar, name='add-visa-seminar-referee'),
    path('hakem/visa-seminar-duzenle/<uuid:uuid>', RefereeViews.updateVisaSeminar, name='update-visa-seminar'),
    path('hakem/visa-seminar-onayla/<uuid:uuid>', RefereeViews.visaSeminarApproval,
         name='referee-visa-seminar-approval'),
    path('hakem/visa-seminar/hakem-sec/<uuid:uuid>', RefereeViews.addRefereeVisaSeminar,
         name='add-referee-visa-seminar'),
    path('hakem/visa-seminar/hakem-kaldir/', RefereeViews.deleteRefereeVisaSeminar,
         name='delete-referee-visa-seminar'),
    path('hakem/visa-Seminar/seminer-sil/', RefereeViews.deleteVisaSeminar, name='delete-visa-seminar'),
    path('hakem/visa-seminar/basvuru-listesi', RefereeViews.returnVisaSeminarApplication,
         name='return-visa-seminar-application'),
    path('hakem/visa-Seminar/hakem-basvuru-reddet/',
         RefereeViews.deleteRefereeApplicationVisaSeminar, name='delete-referee-application-visa-seminar'),
    path('hakem/visa-Seminar/hakem-basvuru-onayla/',
         RefereeViews.approvalRefereeApplicationVisaSeminar, name='approval-referee-application-visa-seminar'),

    path('hakem/belge/<uuid:uuid>', RefereeViews.document, name='document-referee'),

    # Antrenör VİZE SEMİNER

    path('antrenor/visa-seminar', CoachViews.returnVisaSeminar, name='coach-visa-seminar'),
    path('antrenor/visa-seminar/basvuru-listesi', CoachViews.returnVisaSeminarApplication,
         name='return-coach-visa-seminar-application'),
    path('antrenor/visa-seminar-ekle', CoachViews.addVisaSeminar, name='add-visa-seminar-coach'),
    path('antrenor/visa-seminar-duzenle/<uuid:uuid>', CoachViews.updateVisaSeminar, name='update-coach-visa-seminar'),
    path('antrenor/visa-Seminar/seminer-sil/', CoachViews.deleteVisaSeminar, name='delete-coach-visa-seminar'),
    path('antrenor/visa-seminar-onayla/<uuid:uuid>', CoachViews.visaSeminarApproval,
         name='coach-visa-seminar-approval'),
    path('antrenor/visa-seminar/antrenor-sec/<uuid:uuid>', CoachViews.addCoachVisaSeminar,
         name='add-coach-visa-seminar'),
    path('antrenor/visa-seminar/antrenor-kaldir/', CoachViews.deleteCoachVisaSeminar,
         name='coachDeleteVisaSeminar'),
    path('antrenor/visa-Seminar/antrenor-basvuru-reddet/',
         CoachViews.deleteCoachApplicationVisaSeminar, name='delete-coach-application-visa-seminar'),
    path('antrenor/visa-Seminar/antrenor-basvuru-onayla/',
         CoachViews.approvalCoachApplicationVisaSeminar, name='approval-coach-application-visa-seminar'),

    path('antrenor/belge/<uuid:uuid>', CoachViews.document, name='document-coach'),

    path(r'reference/antrenor/basvuru', CoachViews.antrenor, name='coach-application'),

    path(r'antrenor/antrenor-kayit-düzenle/<uuid:uuid>', CoachViews.coachreferenceUpdate,
         name='update-coach-reference'),

    path(r'antrenor/basvuru-onayla', CoachViews.approvelReferenceCoach,
         name='approvel-coach-application'),

    path(r'antrenor/basvuru-reddet', CoachViews.refencedeleteCoach,
         name='refencedeleteCoach'),

    path('hakem/hakem-basvuru', RefereeViews.referencedListReferee, name='referencedListReferee'),
    path('hakem/basvuru-onayla', RefereeViews.refenceapprovalReferee,
         name='refenceapprovalReferee'),

    path('hakem/basvuru-duzenle/<uuid:uuid>', RefereeViews.referenceUpdateReferee,
         name='update-referenceReferee'),

    path('hakem/basvuru-reddet', RefereeViews.refencedeleteReferee,
         name='refencedeleteReferee'),
    #Özel Spor Tesisi

    path('tesis/tesis-ekle', SportFacilityViews.AddSportFacility, name='AddSportFacility'),
    path('tesis/tesis-listesi', SportFacilityViews.return_facility, name='return_facility'),
    path('tesis/tesis-sil', SportFacilityViews.delete_facility, name='delete_facility'),
    path('tesis/tesis-duzenle/<uuid:uuid>', SportFacilityViews.update_sport_facility, name='update_sport_facility'),
    path('tesis/tesis-yetkilisi-sil', SportFacilityViews.delete_facility_manager, name='delete_facility_manager'),
    path('tesis/tesis-yetkili-listesi/<uuid:uuid>', SportFacilityViews.return_facilityUser, name='return_facilityUser'),
    path('tesis/tesis-yetkili-ekle/<uuid:uuid>', SportFacilityViews.AddSportFacilityManager, name='AddSportFacilityManager'),
    path('tesis/tesis-calistirici-sil', SportFacilityViews.delete_facility_coach, name='delete_facility_coach'),
    path('tesis/tesis-calistirici-listesi/<uuid:uuid>', SportFacilityViews.return_facilityCoach, name='return_facilityCoach'),
    path('tesis/tesis-calistirici-ekle/<uuid:uuid>', SportFacilityViews.AddSportFacilityCoach,
         name='AddSportFacilityCoach'),
    path('tesis/tesis-yetkili-duzenle/<uuid:uuid>/<uuid:facility_uuid>', SportFacilityViews.updateSportFacilityManager,name='updateSportFacilityManager'),
    path('tesis/tesis-belge-listesi/<uuid:uuid>', SportFacilityViews.return_facilityDocument, name='return_facilityDocument'),
    path('tesis/tesis-belge-sil', SportFacilityViews.delete_facility_document, name='delete_facility_document'),

    # DOCUMENTS
    path('belgeler', DocumentViews.return_document, name='return_document'),
    path('belge/sil/', DocumentViews.document_delete, name='document_delete'),
    path('belge/guncelle/<uuid:uuid>', DocumentViews.document_update, name='document_update'),

    # Announcement
    path('duyuru/duyurular', AnnouncementViews.returnAnnouncement, name='announcements'),
    path('duyuru/duyuru-ekle', AnnouncementViews.addAnnouncement, name='add_announcements'),
    path('duyuru/duyuru-duzenle/<uuid:uuid>', AnnouncementViews.updateAnnouncement, name='update_announcements'),
    path('duyuru/duyuru-sil/', AnnouncementViews.delete_announcement, name='delete_announcement'),
    path('duyuru/duyuru-getir/', AnnouncementViews.getAnnouncement, name='get_announcement'),

    path('aktarma/spor-salonu', Aktarma.transmissionFacility, name='transmissionFacility'),
    path('aktarma/antrenor', Aktarma.transmissionAntrenor, name='transmissionAntrenor'),

    path('tesis/tesis-getir-api/', TransmissionViews.GetCurrentFacilityDetail, name='tesis-getir-api'),
    path('tesis/tesis-onayla/<uuid:uuid>', SportFacilityViews.pre_facility_approve, name='pre_facility_approve'),
    path('tesis/tesis-basvurulari',SportFacilityViews.pre_facility, name='pre_facility'),

    path('izin/api-izin-listesi/', APIViews.GetPermission.as_view(), name='view_permission-api'),
    path('antrenor/api-antrenor-listesi/', APIViews.GetCoach.as_view(), name='view_coach-api'),
    path('hakem/api-hakem-listesi/', APIViews.GetReferee.as_view(), name='view_referee-api'),
    path('tesis/api-tesis-listesi/', APIViews.GetFacility.as_view(), name='view_sport-facility-api'),
    path('hakem/filtrele/', RefereeViews.return_referee_search, name='return_referee_search'),
    path('antrenor/filtrele/', CoachViews.return_coach_search, name='return_coach_search'),
    path('tesis/filtrele/', SportFacilityViews.return_facility_search, name='return_facility_search'),

]
