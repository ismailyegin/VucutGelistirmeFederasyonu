# -*- coding: utf-8 -*-
import unidecode
from django.db import models

from sbs.models import Branch
from sbs.models.tvfbf.Club import Club
from sbs.models.ekabis.Country import Country
from sbs.models.ekabis.CategoryItem import CategoryItem
from sbs.models.ekabis.City import City
from sbs.models.tvfbf.BaseModel import BaseModel


class ReferenceCoach(BaseModel):
    MALE = 'Erkek'
    FEMALE = 'Kadın'

    AB1 = 'AB Rh+'
    AB2 = 'AB Rh-'
    A1 = 'A Rh+'
    A2 = 'A Rh-'
    B1 = 'B Rh+'
    B2 = 'B Rh-'
    O1 = 'AB Rh+'
    O2 = 'AB Rh+'

    GENDER_CHOICES = (
        (MALE, 'Erkek'),
        (FEMALE, 'Kadın'),
    )
    IsFormal = (
        (True, 'Spor Kulubü'),
        (False, 'Diger(Özel Salon-Dojo-Sportif Dernek)'),
    )

    BLOODTYPE = (
        (AB1, 'AB Rh+'),
        (AB2, 'AB Rh-'),
        (A1, 'A Rh+'),
        (A2, 'A Rh-'),
        (B1, 'B Rh+'),
        (B2, 'B Rh-'),
        (O1, '0 Rh+'),
        (O2, '0 Rh-'),

    )
    WAITED = 'Beklemede'
    APPROVED = 'Onaylandı'
    PROPOUND = 'Onaya Gönderildi'
    DENIED = 'Reddedildi'

    STATUS_CHOICES = (
        (APPROVED, 'Onaylandı'),
        (PROPOUND, 'Onaya Gönderildi'),
        (DENIED, 'Reddedildi'),
        (WAITED, 'Beklemede'),
    )
    status = models.CharField(max_length=128, verbose_name='Onay Durumu', choices=STATUS_CHOICES, default=WAITED)
    iban = models.CharField(max_length=120, null=False, blank=False, verbose_name='İban Adresi')

    # person form
    tc = models.CharField(max_length=120, null=True, blank=True)
    height = models.CharField(max_length=120, null=True, blank=True)
    weight = models.CharField(max_length=120, null=True, blank=True)
    birthplace = models.CharField(max_length=120, null=True, blank=True, verbose_name='Doğum Yeri')
    motherName = models.CharField(max_length=120, null=True, blank=True, verbose_name='Anne Adı')
    fatherName = models.CharField(max_length=120, null=True, blank=True, verbose_name='Baba Adı')
    profileImage = models.ImageField(upload_to='profile/', null=False, blank=False,
                                     verbose_name='Vesikalık Resmi')
    birthDate = models.DateField(null=True, blank=True, verbose_name='Doğum Tarihi')
    bloodType = models.CharField(max_length=128, verbose_name='Kan Grubu', choices=BLOODTYPE, null=True, blank=True)
    gender = models.CharField(max_length=128, verbose_name='Cinsiyeti', choices=GENDER_CHOICES, default=MALE)
    # communicationform
    postalCode = models.CharField(max_length=120, null=True, blank=True)
    phoneNumber = models.CharField(max_length=120, null=True, blank=True)
    phoneNumber2 = models.CharField(max_length=120, null=True, blank=True)
    address = models.TextField(blank=True, null=True, verbose_name='Adres')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Ülke')

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    is_staff = models.BooleanField(default=False,
                                   help_text=('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(default=True,
                                    help_text=('Designates whether this user should be treated as active. '))

    kademe_definition = models.ForeignKey(CategoryItem, on_delete=models.CASCADE, related_name='vucutDefiniton', null=True, blank=True)
    kademe_startDate = models.DateField(null=True, blank=True, verbose_name='Başlangıç Tarihi ')
    kademe_belge = models.FileField(upload_to='dekont/', null=False, blank=False, verbose_name='Belge')  # Sözleşme
    sgk = models.FileField(null=True, blank=True, verbose_name='SGK Belgesi')  # SGK
    belge = models.FileField(null=True, blank=True, verbose_name='Belge')  # ANTRENOR BELGESİ
    kademe_brans = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='gradeVucutBranch')
    vize_brans = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='visaVucutBranch')
    dekont = models.FileField(null=True, blank=True, verbose_name='Dekont')  # dekont

    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
    definition = models.TextField(null=True, blank=True, verbose_name='Reddedilme Sebebi')
    status_date = models.DateField(null=True, blank=True, verbose_name='Onaylanma Tarihi')
    workplace = models.CharField(max_length=150, null=True, blank=True, verbose_name='Çalıştığı Yer')

    kademe_definition2 = models.ForeignKey(CategoryItem, on_delete=models.CASCADE, related_name='bilekDefiniton', null=True, blank=True)
    belge2 = models.FileField(null=True, blank=True, verbose_name='bilekBelge')
    kademe_brans2 = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='gradeBilekBranch')

    vize_brans2 = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='visaBilekBranch')
    dekont2 = models.FileField(null=True, blank=True, verbose_name='Dekont')  # dekont

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        if self.profileImage:
            self.profileImage.name = unidecode.unidecode(self.profileImage.name)
        if self.kademe_belge:
            self.kademe_belge.name = unidecode.unidecode(self.kademe_belge.name)
        if self.sgk:
            self.sgk.name = unidecode.unidecode(self.sgk.name)
        if self.dekont:
            self.dekont.name = unidecode.unidecode(self.dekont.name)
        if self.belge:
            self.belge.name = unidecode.unidecode(self.belge.name)
        super(ReferenceCoach, self).save(*args, **kwargs)
