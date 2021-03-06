from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel


class Country(BaseModel):
    name = models.CharField(max_length=250,blank=True, null=True, verbose_name='Ülke')
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '%s ' % self.name


    class Meta:
        default_permissions = ()

