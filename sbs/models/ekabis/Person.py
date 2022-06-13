from django.contrib.auth.models import User
from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel


class Person(BaseModel):
    MALE = 0
    FEMALE = 1

    AB1 = 'ABRH(+)'
    AB2 = 'ABRH(-)'
    A1 = 'ARH(+)'
    A2 = 'ARH(-)'
    B1 = 'BRH(+)'
    B2 = 'BRH(-)'
    O1 = '0RH(+)'
    O2 = '0RH(-)'

    GENDER_CHOICES = (
        (MALE, 'Erkek'),
        (FEMALE, 'Kadın'),
    )

    BLOODTYPE = (
        (AB1, 'ABRH(+)'),
        (AB2, 'ABRH(-)'),
        (A1, 'ARH(+)'),
        (A2, 'ARH(-)'),
        (B1, 'BRH(+)'),
        (B2, 'BRH(-)'),
        (O1, '0RH(+)'),
        (O2, '0RH(-)'),

    )

    tc = models.CharField(max_length=120, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, db_column='user', null=True, blank=True)
    # phoneNumber = models.CharField(max_length=11, null=False, blank=False)
    # address = models.CharField(max_length=250,blank=True, null=True, verbose_name='Adres')
    height = models.CharField(max_length=120, null=True, blank=True)
    weight = models.CharField(max_length=120, null=True, blank=True)
    birthplace = models.CharField(max_length=120, null=True, blank=True, verbose_name='Doğum Yeri')
    motherName = models.CharField(max_length=120, null=True, blank=True, verbose_name='Anne Adı')
    fatherName = models.CharField(max_length=120, null=True, blank=True, verbose_name='Baba Adı')
    profileImage = models.ImageField(upload_to='profile/', null=True, blank=True, default='profile/user.png',
                                     verbose_name='Profil Resmi')
    birthDate = models.DateField(null=True, blank=True, verbose_name='Doğum Tarihi')
    bloodType = models.CharField(max_length=128, verbose_name='Kan Grubu', choices=BLOODTYPE, default=AB1, null=True,
                                 blank=True)
    gender = models.IntegerField(blank=True, null=True, choices=GENDER_CHOICES)
    # failed_login = models.IntegerField(null=True, blank=True, default=0)
    # failed_time = models.DateTimeField(null=True, blank=True)
    is_unvani = models.CharField(max_length=120, blank=True, null=True)

    iban = models.CharField(max_length=120, null=True, blank=True, verbose_name='İban Adresi')
    hesKodu = models.CharField(max_length=20, null=True, blank=True, verbose_name='HES KODU')
    secretId = models.CharField(null=True, blank=True, max_length=20)

    class Meta:
        default_permissions = ()

    def save(self, *args, **kwargs):
        self.profileImage.name = str(self.profileImage.name.encode('utf-8'))
        super(Person, self).save(*args, **kwargs)

    # def __str__(self):
    #     return '%s' % self.user.get_full_name()
