from django.db import models
from sbs.models.tvfbf.BaseModel import BaseModel


class ReferenceSportFacility(BaseModel):
    status_type = (
        (True, 'Açık'),
        (False, 'Kapalı'),
    )

    name = models.CharField(max_length=250, null=True, blank=True, verbose_name='Özel Spor Tesisi Adı')
    derbis = models.CharField(max_length=100, null=True, blank=True, verbose_name='Derbis No')
    mersis = models.CharField(max_length=100, null=True, blank=True, verbose_name='Mersis No')
    status = models.BooleanField(default=False, verbose_name='Durum', choices=status_type)
    permitDate = models.DateField(null=True, blank=True, verbose_name='Çalışma İzin Bel.Ver.Tar.')
    coordinate = models.TextField(null=True, blank=True, verbose_name='Koordinat')
    registrationNumber = models.CharField(max_length=250, null=True, blank=True, verbose_name='İşyeri Tescil No')
    taxNumber = models.CharField(max_length=250, null=True, blank=True, verbose_name='Vergi Numarası')

    def __str__(self):
        return '%s' % (self.name)
