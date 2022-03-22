from django.db import models
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.models.ekabis.CompanyUser import CompanyUser


class YekaUser(BaseModel):
    user = models.ForeignKey(CompanyUser, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)
    startDate = models.DateField(null=True, blank=True, verbose_name='Başlama Tarihi')
    finisDate = models.DateField(null=True, blank=True, verbose_name='Bitiş  Tarihi')
    file = models.FileField(upload_to='CompanyUser/', null=True, blank=True, verbose_name='Atama Yazısı')
