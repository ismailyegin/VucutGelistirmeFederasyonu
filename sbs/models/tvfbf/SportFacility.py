from django.db import models

from sbs.models import Coach
from sbs.models.ekabis.Communication import Communication
from sbs.models.ekabis.Person import Person
from sbs.models.tvfbf.FacilityDocument import FacilityDocument
from sbs.models.tvfbf.SportFacilityManager import SportFacilityManager
from sbs.models.tvfbf.HavaLevel import HavaLevel
from sbs.models.tvfbf.BaseModel import BaseModel


class SportFacility(BaseModel):
    status_type = (
        (True, 'Açık'),
        (False, 'Kapalı'),
    )

    manager = models.ManyToManyField(SportFacilityManager,related_name='SportFacilityManager')
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True, verbose_name='Özel Spor Tesisi Adı')
    derbis = models.CharField(max_length=100, null=True, blank=True, verbose_name='Derbis No')
    mersis = models.CharField(max_length=100, null=True, blank=True, verbose_name='Mersis No')
    status = models.BooleanField(default=False, verbose_name='Durum', choices=status_type)
    visa = models.ManyToManyField(HavaLevel, related_name='SportFacilityVisa')
    permitDate = models.DateField(null=True, blank=True, verbose_name='Çalışma İzin Bel.Ver.Tar.')
    coordinate = models.TextField(null=True, blank=True, verbose_name='Koordinat')
    registrationNumber = models.CharField(max_length=250, null=True, blank=True, verbose_name='İşyeri Tescil No')
    taxNumber = models.CharField(max_length=250, null=True, blank=True, verbose_name='Vergi Numarası')
    coach=models.ManyToManyField(Coach,related_name='facilityCoach')
    document=models.ManyToManyField(FacilityDocument,related_name='facilityDocument')
    def __str__(self):
        return '%s' % (self.name)
