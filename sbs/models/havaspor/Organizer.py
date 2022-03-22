from django.db import models

from sbs.models.ekabis.Communication import Communication
from sbs.models.ekabis.Person import Person
from sbs.models.havaspor.BaseModel import BaseModel
from sbs.models.havaspor.Branch import Branch


class Organizer(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, null=True, blank=True)
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ManyToManyField(Branch)
    companyName = models.CharField(null=True, blank=True, max_length=255, verbose_name='Firma Ünvanı')
    companyRepresentative = models.CharField(null=True, blank=True, max_length=255, verbose_name='Firma Yetkilisi')
    companyTaxOffice = models.CharField(null=True, blank=True, max_length=255, verbose_name='Firma Vergi Dairesi')
    companyTaxNumber = models.CharField(null=True, blank=True, max_length=255, verbose_name='Firma Vergi Numarası')
    companyPhoneNumber = models.CharField(null=True, blank=True, max_length=255, verbose_name='Firma Telefon Numarası')
    companyEmail = models.EmailField(null=True, blank=True, verbose_name='Firma E-posta')
    companyAddress = models.TextField(blank=True, null=True, verbose_name='Firma Adresi')
    infoLevel = models.BooleanField(default=True, null=True, blank=True)
    infoStatus = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return '%s ' % self.companyName
