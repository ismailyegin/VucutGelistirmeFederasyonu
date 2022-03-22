from django.contrib.auth.models import User
from django.db import models

from sbs.models.ekabis.City import City
from sbs.models.havaspor.BaseModel import BaseModel
from sbs.models.havaspor.Branch import Branch


class AirSportsCompetition(BaseModel):
    secretId = models.CharField(max_length=10, null=True, blank=True)
    branch = models.ManyToManyField(Branch)
    name = models.CharField(max_length=255, verbose_name='Etkinlik Başlığı', null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl', db_column='city', null=True, blank=True)
    startDate = models.DateField(blank=True, null=True, verbose_name='Etkinlik Başlangıç Tarihi')
    finishDate = models.DateField(blank=True, null=True, verbose_name='Etkinlik Bitiş Tarihi')
    description = models.TextField(verbose_name='Etkinlik Açıklama', null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Etkinliği Oluşturan Kişi',
                                db_column='auth_user', null=True, blank=True)
    createdDate = models.DateTimeField(blank=True, null=True, verbose_name='Etkinlik Oluşturulma Tarihi')
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return '%s' % self.name
