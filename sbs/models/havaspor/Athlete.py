from django.db import models

from sbs.models.havaspor.Club import Club
from sbs.models.ekabis.Communication import Communication
from sbs.models.ekabis.Person import Person
from sbs.models.havaspor.CertificateDegree import CertificateDegree
from sbs.models.havaspor.Branch import Branch
from sbs.models.havaspor.BaseModel import BaseModel
from sbs.models.havaspor.License import License


class Athlete(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, null=True, blank=True)
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE, null=True, blank=True)
    licenses = models.ManyToManyField(License)

    branch = models.ManyToManyField(Branch)
    airTribuneId = models.CharField(null=True, blank=True, max_length=255, verbose_name='airtribune.com')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, db_column='Club', null=True, blank=True)
    insuranceCompany = models.CharField(null=True, blank=True, max_length=255)
    insurancePolicy = models.CharField(null=True, blank=True, max_length=255)
    flightJump = models.CharField(max_length=5000, null=True, blank=True, verbose_name='Uçuş/Atlayış Yer')  # UçuşAtlayış
    successDegree = models.CharField(max_length=5000, null=True, blank=True, verbose_name='Başarılarınız')
    last12month = models.CharField(null=True, blank=True, max_length=255, verbose_name='Son 12 Ay Uçuş Süresi')
    totalSortie = models.CharField(null=True, blank=True, max_length=255, verbose_name='Toplam Uçuş Süresi')
    certificateDegree = models.ManyToManyField(CertificateDegree)
    infoLevel = models.BooleanField(default=True, null=True, blank=True)
    infoStatus = models.BooleanField(default=True, null=True, blank=True)


    def __str__(self):
        return '%s %s' % (self.person.user.first_name, self.person.user.last_name)
