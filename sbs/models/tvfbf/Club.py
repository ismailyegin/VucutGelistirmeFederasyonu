from django.db import models

from sbs.models.ekabis.Communication import Communication
from sbs.models.tvfbf.Branch import Branch
from sbs.models.tvfbf.SportClubUser import SportClubUser
from sbs.models.tvfbf.BaseModel import BaseModel
from sbs.models.tvfbf.Coach import Coach


class Club(BaseModel):
    IsFormal = (
        (True, 'Spor Kulubü'),
        (False, 'Diger(Özel Salon-Dojo-Sportif Dernek)'),
    )

    name = models.CharField(blank=True, null=True, max_length=120)
    shortName = models.CharField(blank=True, null=True, max_length=120)
    foundingDate = models.CharField(blank=True, null=True, max_length=120)
    clubMail = models.CharField(blank=True, null=True, max_length=120)
    logo = models.ImageField(upload_to='club/', null=True, blank=True, verbose_name='Kulüp Logo')
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE, db_column='communication', null=True,
                                         blank=True)
    coachs = models.ManyToManyField(Coach)
    branch = models.ManyToManyField(Branch,blank=True)
    isFormal = models.BooleanField(default=True, choices=IsFormal)
    clubUser = models.ManyToManyField(SportClubUser)
    dataAccessControl = models.BooleanField(blank=True, null=True, default=False)
    password = models.CharField(blank=True, null=True, max_length=120)
    username = models.CharField(blank=True, null=True, max_length=120)
    isRegister = models.BooleanField(default=False)
    petition = models.FileField(upload_to='club/', null=True, blank=True, verbose_name='Yetki Belgesi ')
    infoStatus = models.BooleanField(default=True, null=True, blank=True)
    infoLevel = models.BooleanField(default=True, null=True, blank=True)
    secretId = models.CharField(null=True, blank=True, max_length=20)
    derbis = models.CharField(max_length=100, null=True, blank=True, verbose_name='Derbis Kütük No')
    guidId = models.CharField(max_length=100, null=True, blank=True, verbose_name='Kulüp Guid No')

    def __str__(self):
        return '%s' % (self.name)

    # class Meta:
    #     default_permissions = ()
    #     db_table = 'sportclub'
    #     managed = False
