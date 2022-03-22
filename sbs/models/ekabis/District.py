from django.db import models
from sbs.models.ekabis.City import City


class District(models.Model):
    name = models.CharField(max_length=250,blank=True, null=True, verbose_name='İlçe')
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)

    def __str__(self):
        return '%s ' % self.name


