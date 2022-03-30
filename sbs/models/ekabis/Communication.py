from django.db import models

from sbs.models.ekabis.Country import Country
from sbs.models.ekabis.City import City
from sbs.models.tvfbf.BaseModel import BaseModel


class Communication(BaseModel):
    secretId = models.CharField(null=True, blank=True, max_length=20)
    postalCode = models.CharField(max_length=120, null=True, blank=True)
    phoneNumber = models.CharField(max_length=120, null=True, blank=True)
    phoneNumber2 = models.CharField(max_length=120, null=True, blank=True)
    phoneHome = models.CharField(max_length=120, null=True, blank=True)
    phoneJop = models.CharField(max_length=120, null=True, blank=True)
    address = models.TextField(blank=True, null=True, verbose_name='Adres')
    addressHome = models.TextField(blank=True, null=True, verbose_name='AdresHome')
    addressJop = models.TextField(blank=True, null=True, verbose_name='AdresJop')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl', db_column='city', null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Ülke', db_column='country', null=True,
                                blank=True)

    town = models.CharField(max_length=120, null=True, blank=True)
    neighborhood = models.CharField(max_length=120, null=True, blank=True)
    acildurum_kisi = models.CharField(max_length=250, null=True, blank=True, verbose_name='Acil Durum Kişisi')
    acildurum_phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='Acil Durum Telefonu')
    fax = models.CharField(max_length=250, null=True, blank=True)
    webSite = models.CharField(max_length=250, null=True, blank=True, verbose_name='web sitesi')

    # class Meta:
    #     default_permissions = ()
    #     db_table = 'communication'
    #     managed = False
