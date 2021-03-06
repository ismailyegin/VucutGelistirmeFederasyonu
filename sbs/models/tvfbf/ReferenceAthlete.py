from django.db import models

from sbs.models.ekabis.City import City
from sbs.models.ekabis.Country import Country
from sbs.models.ekabis.CategoryItem import CategoryItem
from sbs.models.tvfbf.Club import Club
from sbs.models.tvfbf.BaseModel import BaseModel


class ReferenceAthlete(BaseModel):
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

    VUCUT = 'VÜCUT GELİŞTİRME VE FİTNESS'
    BILEK = 'BİLEK GÜREŞİ'

    BRANCHTYPE = (
        (VUCUT, 'VÜCUT GELİŞTİRME VE FİTNESS'),
        (BILEK, 'BİLEK GÜREŞİ'),

    )

    FERDI = 'KULÜP LİSANSI'
    KULUP = 'FERDİ LİSANS'

    LICENSETYPE = (
        (FERDI, 'FERDİ LİSANS'),
        (KULUP, 'KULÜP LİSANSI'),

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
    profileImage = models.ImageField(upload_to='profile/', null=False, blank=False,verbose_name='Profil Resmi')
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

    #LİSANS
    licenseBranch = models.CharField(verbose_name='Branş', null=True,blank=True,choices=BRANCHTYPE,max_length=250)
    license_club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True,blank=True)
    isActive = models.BooleanField(default=False)
    licenseNo = models.CharField(blank=True, null=True, max_length=255)
    expireDate = models.DateField(blank=True, null=True)
    startDate = models.DateField(blank=True, null=True)
    licenseStatus = models.CharField(max_length=128, verbose_name='Onay Durumu', choices=STATUS_CHOICES, default=WAITED)
    lisansPhoto = models.FileField(upload_to='lisans/', null=True, blank=True, verbose_name='Lisans')
    reddetwhy = models.CharField(blank=True, null=True, max_length=255)
    isFerdi = models.BooleanField(default=False)
    licenseName = models.TextField(null=True, blank=True, verbose_name='Lisans')
    license_city=models.CharField(null=True,blank=True,verbose_name='Lisans İl',max_length=100)
    license_year=models.CharField(blank=True, null=True, max_length=255)


    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    is_staff = models.BooleanField(default=False,
                                   help_text=('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(default=False,
                                    help_text=('Designates whether this user should be treated as active. '))

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

