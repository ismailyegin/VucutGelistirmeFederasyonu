from django.db import models

from sbs.models.havaspor.BaseModel import BaseModel


class Branch(BaseModel):
    secretId = models.CharField(max_length=10)
    title = models.CharField(blank=True, null=True, max_length=120, verbose_name='Branş Adı')
    is_parent = models.BooleanField(default=True)
    is_show = models.BooleanField(default=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True)
    sort = models.IntegerField(blank=True, null=True, verbose_name='Branş Sort')

    def __str__(self):
        return '%s ' % self.title