from django.db import models

from sbs.models.ekabis.Company import Company
from sbs.models.ekabis.YekaCompetition import YekaCompetition
from sbs.models.ekabis.BaseModel import BaseModel
from sbs.services.services import validate_file_size

#TEMINAT MODELI - yeka kullanim haklari sozlesmesinde kullanılacak
class Collateral(BaseModel):
    guaranteeDate = models.DateField(null=True, blank=True)
    bank = models.CharField(max_length=250, null=True, blank=True)
    quantity = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=2,
                                   verbose_name='Teminat Miktarı')
    branch = models.CharField(max_length=250, null=True, blank=True)
    reference = models.CharField(max_length=250, null=True, blank=True)
    pikur = models.CharField(max_length=250, null=True, blank=True)
    guaranteeTime = models.IntegerField(verbose_name='Taminat Süresi', null=True, blank=True)
    definition = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(max_length=250, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, blank=True)
    competition = models.ForeignKey(YekaCompetition, on_delete=models.DO_NOTHING, null=True, blank=True)
    guaranteeFile = models.FileField(null=True, blank=True, verbose_name='Teminat Mektubu', upload_to="teminat/",
                                     validators=[validate_file_size])
    guaranteeCount = models.IntegerField()
    rebateDate=models.DateField(null=True,blank=True,verbose_name='İade Tarihi') # durum iade seçilmiş ise
