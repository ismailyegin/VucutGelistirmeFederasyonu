from django.db import models
from unicode_tr import unicode_tr

from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.YekaCompetition import YekaCompetition
from sbs.models.ekabis.City import City

class ConnectionRegion(BaseModel):
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name='Bağlantı Bölgesi')
    capacity = models.IntegerField(null=False, blank=False, verbose_name='Kapasite')
    cities=models.ManyToManyField(City)
    yekacompetition=models.ManyToManyField(YekaCompetition,related_name='competition_regions')
    def __str__(self):
        return '%s ' % self.name

    def save(self, force_insert=False, force_update=False):
        if self.name:
            self.name = unicode_tr(self.name).upper()

        super(ConnectionRegion, self).save(force_insert, force_update)
