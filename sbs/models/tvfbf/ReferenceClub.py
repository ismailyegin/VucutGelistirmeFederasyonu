import unidecode
from django.db import models

from sbs.models.ekabis.Country import Country
from sbs.models.tvfbf.ClubRole import ClubRole
from sbs.models.ekabis.City import City



class ReferenceClub(models.Model):
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

    IsCoach = (
        (True, 'Evet '),
        (False, 'Hayır'),
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
    status = models.CharField(max_length=128, verbose_name='Onay Durumu', choices=STATUS_CHOICES, default=WAITED,null=True,blank=True)

    # person form
    tc = models.CharField(max_length=120, null=True, blank=True)
    birthplace = models.CharField(max_length=120, null=True, blank=True,verbose_name='Doğum Yeri')
    motherName = models.CharField(max_length=120, null=True, blank=True,verbose_name='Anne Adı')
    fatherName = models.CharField(max_length=120, null=True, blank=True,verbose_name='Baba Adı')
    profileImage = models.ImageField(upload_to='profile/', null=True,blank=True,verbose_name='Profil Resmi')
    birthDate = models.DateField(null=True, blank=True, verbose_name='Doğum Tarihi')
    bloodType = models.CharField(max_length=128, verbose_name='Kan Grubu', choices=BLOODTYPE, null=True, blank=True)
    gender = models.CharField(max_length=128, verbose_name='Cinsiyeti', choices=GENDER_CHOICES, default=MALE,null=True,blank=True)
    # communicationform
    phoneNumber = models.CharField(max_length=120, null=True, blank=True)
    phoneNumber2 = models.CharField(max_length=120, null=True, blank=True)
    address = models.TextField(blank=True, null=True, verbose_name='Adres')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl',related_name='user_city',null=True,blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Ülke',related_name='user_country',null=True,blank=True)

    # sportClup
    name = models.CharField(blank=True, null=True, max_length=120)
    shortName = models.CharField(blank=True, null=True, max_length=120)
    foundingDate = models.DateField(blank=True, null=True, max_length=120,verbose_name='Kuruluş Tarihi')
    clubMail = models.CharField(blank=True, null=True, max_length=120)
    logo = models.ImageField(upload_to='club/', null=True, blank=True, verbose_name='Kulüp Logo')
    derbis = models.CharField(max_length=100, null=True, blank=True, verbose_name='Derbis Kütük No')

    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)


    clubpostalCode = models.CharField(max_length=120, null=True, blank=True)
    clubphoneNumber = models.CharField(max_length=120, null=True, blank=True)
    clubphoneNumber2 = models.CharField(max_length=120, null=True, blank=True)
    clubaddress = models.TextField(blank=True, null=True, verbose_name='Adres')
    clubcity = models.CharField(max_length=100, verbose_name='İl',null=True,blank=True)
    clubcountry = models.CharField(max_length=100, verbose_name='Ülke',null=True,blank=True)

    clubTown=models.CharField(max_length=200,null=True,blank=True)
    clubFax=models.CharField(max_length=11,null=True,blank=True)
    isCoach = models.BooleanField(default=False, choices=IsCoach,null=True,blank=True)

     #userForm
    first_name = models.CharField( max_length=30, blank=True,null=True)
    last_name = models.CharField( max_length=150, blank=True,null=True)
    email = models.EmailField( max_length=254,blank=True,null=True)
    is_staff = models.BooleanField(default=False, help_text=('Designates whether the user can log into this admin site.'),null=True,blank=True)
    is_active = models.BooleanField(default=False,help_text=('Designates whether this user should be treated as active. '),null=True,blank=True)

    # gerekli evraklar
    dekont = models.FileField(upload_to='dekont/', null=True, blank=True, verbose_name='Dekont ')
    # Sportclup user
    role = models.ForeignKey(ClubRole, on_delete=models.DO_NOTHING, verbose_name='Üye Rolü')

    kademe_definition = models.CharField(null=True, blank=True, max_length=150)
    kademe_startDate = models.DateField(null=True, blank=True, verbose_name='Başlangıç Tarihi ')
    kademe_belge = models.FileField(upload_to='dekont/', null=True, blank=True, verbose_name='Belge')
    iban = models.CharField(max_length=120, null=True, blank=True, verbose_name='İban Adresi')


    def save(self, *args, **kwargs):
        if self.profileImage:
            self.profileImage.name = unidecode.unidecode(self.profileImage.name)
        if self.logo:
            self.logo.name = unidecode.unidecode(self.logo.name)
        if self.dekont:
            self.dekont.name = unidecode.unidecode(self.dekont.name)
        if self.kademe_belge:
            self.kademe_belge.name = unidecode.unidecode(self.kademe_belge.name)
        super(ReferenceClub, self).save(*args, **kwargs)




